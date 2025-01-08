"""
Module to create and update building energy models, and perform building energy simulation in sequence or parallel.

Delft University of Technology
Dr. Miguel Martin
"""

import multiprocessing
import re
from abc import ABCMeta, abstractmethod
import os
import shutil
from subprocess import Popen
import glob
import platform
import json

import pytz
from pymoo.core.problem import ElementwiseProblem
from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.operators.crossover.sbx import SBX
from pymoo.operators.mutation.pm import PM
from pymoo.operators.sampling.rnd import FloatRandomSampling
from pymoo.termination import get_termination
from pymoo.optimize import minimize

import numpy as np
import subprocess
from datetime import datetime, date, timedelta
import string
import pandas as pd

import shutil
from pvlib.location import Location
from pvlib.iotools import read_epw

import scipy.signal as sig
from scipy.constants import Stefan_Boltzmann as sigma
from scipy.interpolate import interp1d

from sciencespy.dom import *
from sciencespy.utils import *

from eppy import modeleditor
from eppy.modeleditor import IDF

from pint import UnitRegistry
ureg = UnitRegistry()
ureg.define('degree = dimensionless')
ureg.define('percent = 1 / 100')
ureg.define('tenth = 1 / 10')

class BuildingEnergyDataUnknownItemError(Exception):
    """
    Exception raised when getting building energy data that are unkown.
    """
    def __init__(self, message=''):
        Exception.__init__(self, message)

class BuildingEnergyDataOutOfBoundsError(Exception):
    """
    Exception raised when inserting new building energy data that are out of founds.
    """
    def __init__(self, message=''):
        Exception.__init__(self, message)

class BuildingEnergyData():
    """
    Class containing weather data.
    """

    def __init__(self, timestamps):
        """
        :param timestamps: list of timestamps at which weather data were collected.
        """
        self._timestamps = timestamps
        self._total_sensible_load = None
        self._total_latent_load = None
        self._average_wall_surface_temperature = None
        self._internal_mass_temperature = None

    def keys(self):
        """
        :return: list of building energy parameters stored in the dataset.
        """
        all_keys = ['total_sensible_load',
                    'total_latent_load',
                    'average_wall_surface_temperature',
                    'internal_mass_temperature']
        availble_keys = []
        for k in all_keys:
            if self[k] is not None:
                availble_keys.append(k)
        return availble_keys

    def __getitem__(self, item):
        """
        :return: timeseries corresponding to a stored building energy data.
            - dry_bulb_temperature: dry bulb temperature (in degrees Celsius)
        """
        if item == 'total_sensible_load':
            return None if self._total_sensible_load is None else QSeries(index=self._timestamps, data=self._total_sensible_load)
        elif item == 'total_latent_load':
            return None if self._total_latent_load is None else QSeries(index=self._timestamps, data=self._total_latent_load)
        elif item == 'average_wall_surface_temperature':
            return None if self._average_wall_surface_temperature is None else QSeries(index=self._timestamps, data=self._average_wall_surface_temperature)
        elif item == 'internal_mass_temperature':
            return None if self._internal_mass_temperature is None else QSeries(index=self._timestamps, data=self._internal_mass_temperature)
        else:
            raise BuildingEnergyDataUnknownItemError(message = 'Building energy data ' + item + ' are unknown.')

    def __setitem__(self, key, value):
        """
        Modify building energy data.
        :param key: name of weather data to be modified.
            - dry_bulb_temperature: dry bulb temperature.
        :param value: timeseries containing new weather data to be set with units.
        """
        if value is not None:
            start_date = self._timestamps[0]
            new_start_date = value.index[0]
            if new_start_date < start_date:
                raise BuildingEnergyDataOutOfBoundsError(message="New " + key + " starts at "
                                                          + new_start_date.strftime('%Y-%m-%m %H:%M:%S')
                                                          + " and it should be later than "
                                                          + start_date.strftime('%Y-%m-%m %H:%M:%S'))
            end_date = self._timestamps[-1]
            new_end_date = value.index[-1]
            if new_end_date > end_date:
                raise BuildingEnergyDataOutOfBoundsError(message="New " + key + " starts at "
                                                          + new_end_date.strftime('%Y-%m-%m %H:%M:%S')
                                                          + " and it should be sooner than "
                                                          + end_date.strftime('%Y-%m-%m %H:%M:%S'))
            indexes_to_set = (self._timestamps >= new_start_date) & (self._timestamps <= new_end_date)
            timestamps_to_set = self._timestamps[indexes_to_set].astype('int64') / 10**9
            timestamps_to_interp = value.index.astype('int64') / 10**9
            if key == 'total_sensible_load':
                new_values = np.interp(timestamps_to_set, timestamps_to_interp, value.data.to(ureg.watt).m) * ureg.watt
                if self._total_sensible_load is None:
                    self._total_sensible_load = new_values
                else:
                    self._total_sensible_load[indexes_to_set] = new_values
            elif key == 'total_latent_load':
                new_values = np.interp(timestamps_to_set, timestamps_to_interp, value.data.to(ureg.watt).m) * ureg.watt
                if self._total_latent_load is None:
                    self._total_latent_load = new_values
                else:
                    self._total_latent_load[indexes_to_set] = new_values
            elif key == 'average_wall_surface_temperature':
                new_values = np.interp(timestamps_to_set, timestamps_to_interp, value.data.to(ureg.degC).m) * ureg.degC
                if self._average_wall_surface_temperature is None:
                    self._average_wall_surface_temperature = new_values
                else:
                    self._average_wall_surface_temperature[indexes_to_set] = new_values
            elif key == 'internal_mass_temperature':
                new_values = np.interp(timestamps_to_set, timestamps_to_interp, value.data.to(ureg.degC).m) * ureg.degC
                if self._internal_mass_temperature is None:
                    self._internal_mass_temperature = new_values
                else:
                    self._internal_mass_temperature[indexes_to_set] = new_values
            else:
                raise BuildingEnergyDataUnknownItemError(message = 'Building energy data ' + key + ' are unknown.')

    def save(self, file_name, out_dir='.'):
        """
        Save building energy data.
        :param file_name: file name where building energy data must be saved
        :param out_dir: output directory where building energy data must be saved
        """
        df = pd.DataFrame({'Date/Time': self._timestamps.strftime('%Y-%m-%d %H:%M:%S').tolist(),
                           'Total Sensible Load': self._total_sensible_load.m.tolist(),
                           'Total Latent Load': self._total_latent_load.m.tolist(),
                           'Average Wall Surface Temperature': self._average_wall_surface_temperature.m.tolist(),
                           'Internal Thermal Mass': self._internal_mass_temperature.m.tolist()})
        df.to_csv(os.path.join(out_dir, file_name), index=False)

class BuildingEnergyDataLoader():
    """
    Class to load building energy data.

    Attributes:
        building_energy_file: file containing weather data.
    """
    __metaclass__ = ABCMeta

    def __init__(self, building_energy_file):
        """
        :param building_energy_file: file containg building energy data.
        """
        self.building_energy_file = building_energy_file

    def load(self):
        building_energy_data = self.get_instance()
        building_energy_data['total_sensible_load'] = self.get_total_sensible_load()
        building_energy_data['total_latent_load'] = self.get_total_latent_load()
        building_energy_data['average_wall_surface_temperature'] = self.get_average_wall_surface_temperature()
        return building_energy_data

    @abstractmethod
    def get_instance(self):
        """
        :return: instance of weather data
        """
        pass

    @abstractmethod
    def get_total_sensible_load(self):
        """
        :return: total sensible load.
        """
        pass

    @abstractmethod
    def get_total_latent_load(self):
        """
        :return: total latent load.
        """
        pass

    @abstractmethod
    def get_average_wall_surface_temperature(self):
        """
        :return: average wall surface temperature.
        """
        pass

class EnergyPlusDataLoader(BuildingEnergyDataLoader):
    """
    Class to load building energy data generated by EnergyPlus.

    Attributes:
        building_energy_file: file containing building energy data.
    """
    __metaclass__ = ABCMeta

    def __init__(self, building_energy_file, year=datetime.today().year, timezone='GMT'):
        """
        :param building_energy_file: file containing building energy data.
        """
        BuildingEnergyDataLoader.__init__(self, building_energy_file)
        self.year = year
        self.timestamps = None
        self.data = None
        self.timezone = timezone

    def get_instance(self):
        """
        :return: instance of weather data
        """
        self.data = pd.read_csv(self.building_energy_file)
        timestamps = []
        for i, row in self.data.T.items():
            timestamp = str(self.year) + '/' + row['Date/Time'].lstrip()
            try:
                timestamps.append(datetime.strptime(timestamp, '%Y/%m/%d  %H:%M:%S'))
            except ValueError:
                tempts = timestamp.replace(' 24', ' 23')
                timestamps.append(datetime.strptime(tempts, '%Y/%m/%d  %H:%M:%S') + timedelta(hours=1))
        self.timestamps = pd.DatetimeIndex(timestamps).tz_localize(self.timezone)
        return BuildingEnergyData(timestamps=self.timestamps)

    def get_total_sensible_load(self):
        """
        :return: total sensible load.
        """
        total_sensible_load = np.zeros(len(self.timestamps))
        for col_name in list(self.data.columns):
            if 'Zone Ideal Loads Zone Sensible Heating Rate' in col_name:
                total_sensible_load += self.data[col_name].values
            if 'Zone Ideal Loads Zone Sensible Cooling Rate' in col_name:
                total_sensible_load += self.data[col_name].values
        return QSeries(index=self.timestamps, data=total_sensible_load * ureg.watt)

    def get_total_latent_load(self):
        """
        :return: total latent load.
        """
        total_latent_load = np.zeros(len(self.timestamps))
        for col_name in list(self.data.columns):
            if 'Zone Ideal Loads Zone Latent Heating Rate' in col_name:
                total_latent_load += self.data[col_name].values
            if 'Zone Ideal Loads Zone Latent Cooling Rate' in col_name:
                total_latent_load += self.data[col_name].values
        return QSeries(index=self.timestamps, data=total_latent_load * ureg.watt)

    def get_average_wall_surface_temperature(self):
        """
        :return: average wall surface temperature.
        """
        average_surface_temperature = np.zeros(len(self.timestamps))
        count = 0.0
        for col_name in list(self.data.columns):
            if ('EXTWALL' in col_name) and ('Surface Outside Face Temperature' in col_name):
                average_surface_temperature += self.data[col_name].values
                count += 1.0
        return QSeries(index=self.timestamps, data=(average_surface_temperature / count) * ureg.degC)


class WeatherDataUnknownItemError(Exception):
    """
    Exception raised when getting weather data that are unkown.
    """
    def __init__(self, message=''):
        Exception.__init__(self, message)

class WeatherDataOutOfBoundsError(Exception):
    """
    Exception raised when inserting new weather data that are out of founds.
    """
    def __init__(self, message=''):
        Exception.__init__(self, message)

class WeatherData():
    """
    Class containing weather data.
    """
    __metaclass__ = ABCMeta

    def __init__(self, timestamps):
        """
        :param timestamps: list of timestamps at which weather data were collected.
        """
        self._timestamps = timestamps
        self._dry_bulb_temperature = None
        self._dew_point_temperature = None
        self._relative_humidity = None
        self._specific_humidity = None
        self._atmospheric_station_pressure = None
        self._extraterrestrial_horizontal_radiation = None
        self._extraterrestrial_direct_normal_radiation = None
        self._horizontal_infrared_radiation_intensity = None
        self._global_horizontal_radiation = None
        self._direct_normal_radiation = None
        self._diffuse_horizontal_radiation = None
        self._global_horizontal_illuminance = None
        self._direct_normal_illuminance = None
        self._diffuse_horizontal_illuminance = None
        self._zenith_illuminance = None
        self._wind_direction = None
        self._wind_speed = None
        self._total_sky_cover = None
        self._opaque_sky_cover = None
        self._visibility = None
        self._ceiling_height = None
        self._precipitable_water = None
        self._aerosol_optical_depth = None
        self._snow_depth = None
        self._albedo = None
        self._days_since_last_snowfall = None
        self._liquid_precipitation_depth = None
        self._liquid_precipitation_quantity = None
        self._zenith_angle_sun = None
        self._azimuth_angle_sun = None
        self._sky_temperature = None

    def keys(self):
        """
        :return: list of weather parameters stored in the dataset.
        """
        all_keys = ['dry_bulb_temperature',
                    'dew_point_temperature',
                    'relative_humidity',
                    'specific_humidity',
                    'atmospheric_station_pressure',
                    'extraterrestrial_horizontal_radiation',
                    'extraterrestrial_direct_normal_radiation',
                    'horizontal_infrared_radiation_intensity',
                    'global_horizontal_radiation',
                    'direct_normal_radiation',
                    'diffuse_horizontal_radiation',
                    'global_horizontal_illuminance',
                    'direct_normal_illuminance',
                    'diffuse_horizontal_illuminance',
                    'zenith_illuminance',
                    'wind_direction',
                    'wind_speed',
                    'total_sky_cover',
                    'opaque_sky_cover',
                    'visibility',
                    'ceiling_height',
                    'precipitable_water',
                    'aerosol_optical_depth',
                    'snow_depth',
                    'days_since_last_snowfall',
                    'albedo',
                    'liquid_precipitation_depth',
                    'liquid_precipitation_quantity',
                    'zenith_angle_sun',
                    'azimuth_angle_sun',
                    'sky_temperature']
        availble_keys = []
        for k in all_keys:
            if self[k] is not None:
                availble_keys.append(k)
        return availble_keys

    def __getitem__(self, item):
        """
        :return: timeseries corresponding to a stored weather data.
            - dry_bulb_temperature: dry bulb temperature (in degrees Celsius)
        """
        if item == 'dry_bulb_temperature':
            return None if self._dry_bulb_temperature is None else QSeries(index=self._timestamps, data=self._dry_bulb_temperature)
        elif item == 'dew_point_temperature':
            return None if self._dew_point_temperature is None else QSeries(index=self._timestamps, data=self._dew_point_temperature)
        elif item == 'relative_humidity':
            return None if self._relative_humidity is None else QSeries(index=self._timestamps, data=self._relative_humidity)
        elif item == 'specific_humidity':
            return None if self._specific_humidity is None else QSeries(index=self._timestamps, data=self._specific_humidity)
        elif item == 'atmospheric_station_pressure':
            return None if self._atmospheric_station_pressure is None else QSeries(index=self._timestamps, data=self._atmospheric_station_pressure)
        elif item == 'extraterrestrial_horizontal_radiation':
            return None if self._extraterrestrial_horizontal_radiation is None else QSeries(index=self._timestamps, data=self._extraterrestrial_horizontal_radiation)
        elif item == 'extraterrestrial_direct_normal_radiation':
            return None if self._extraterrestrial_direct_normal_radiation is None else QSeries(index=self._timestamps, data=self._extraterrestrial_direct_normal_radiation)
        elif item == 'horizontal_infrared_radiation_intensity':
            return None if self._horizontal_infrared_radiation_intensity is None else QSeries(index=self._timestamps, data=self._horizontal_infrared_radiation_intensity)
        elif item == 'global_horizontal_radiation':
            return None if self._global_horizontal_radiation is None else QSeries(index=self._timestamps, data=self._global_horizontal_radiation)
        elif item =='direct_normal_radiation':
            return None if self._direct_normal_radiation is None else QSeries(index=self._timestamps, data=self._direct_normal_radiation)
        elif item == 'diffuse_horizontal_radiation':
            return None if self._diffuse_horizontal_radiation is None else QSeries(index=self._timestamps, data=self._diffuse_horizontal_radiation)
        elif item == 'global_horizontal_illuminance':
            return None if self._global_horizontal_illuminance is None else QSeries(index=self._timestamps, data=self._global_horizontal_illuminance)
        elif item == 'direct_normal_illuminance':
            return None if self._direct_normal_illuminance is None else QSeries(index=self._timestamps, data=self._direct_normal_illuminance)
        elif item == 'diffuse_horizontal_illuminance':
            return None if self._diffuse_horizontal_illuminance is None else QSeries(index=self._timestamps, data=self._diffuse_horizontal_illuminance)
        elif item == 'zenith_illuminance':
            return None if self._zenith_illuminance is None else QSeries(index=self._timestamps, data=self._zenith_illuminance)
        elif item == 'wind_direction':
            return None if self._wind_direction is None else QSeries(index=self._timestamps, data=self._wind_direction)
        elif item == 'wind_speed':
            return None if self._wind_speed is None else QSeries(index=self._timestamps, data=self._wind_speed)
        elif item == 'total_sky_cover':
            return None if self._total_sky_cover is None else QSeries(index=self._timestamps, data=self._total_sky_cover)
        elif item == 'opaque_sky_cover':
            return None if self._opaque_sky_cover is None else QSeries(index=self._timestamps, data=self._opaque_sky_cover)
        elif item == 'visibility':
            return None if self._visibility is None else QSeries(index=self._timestamps, data=self._visibility)
        elif item == 'ceiling_height':
            return None if self._ceiling_height is None else QSeries(index=self._timestamps, data=self._ceiling_height)
        elif item == 'precipitable_water':
            return None if self._precipitable_water is None else QSeries(index=self._timestamps, data=self._precipitable_water)
        elif item == 'aerosol_optical_depth':
            return None if self._aerosol_optical_depth is None else QSeries(index=self._timestamps, data=self._aerosol_optical_depth)
        elif item == 'snow_depth':
            return None if self._snow_depth is None else QSeries(index=self._timestamps, data=self._snow_depth)
        elif item == 'days_since_last_snowfall':
            return None if self._days_since_last_snowfall is None else QSeries(index=self._timestamps, data=self._days_since_last_snowfall)
        elif item == 'albedo':
            return None if self._albedo is None else QSeries(index=self._timestamps, data=self._albedo)
        elif item == 'liquid_precipitation_depth':
            return None if self._liquid_precipitation_depth is None else QSeries(index=self._timestamps, data=self._liquid_precipitation_depth)
        elif item == 'liquid_precipitation_quantity':
            return None if self._liquid_precipitation_quantity is None else QSeries(index=self._timestamps, data=self._liquid_precipitation_quantity)
        elif item == 'zenith_angle_sun':
            return None if self._zenith_angle_sun is None else QSeries(index=self._timestamps, data=self._zenith_angle_sun)
        elif item == 'azimuth_angle_sun':
            return None if self._azimuth_angle_sun is None else QSeries(index=self._timestamps, data=self._azimuth_angle_sun)
        elif item == 'sky_temperature':
            return None if self._sky_temperature is None else QSeries(index=self._timestamps, data=self._sky_temperature)
        else:
            raise WeatherDataUnknownItemError(message = 'Weather data ' + item + ' are unknown.')

    def __setitem__(self, key, value):
        """
        Modify weather data.
        :param key: name of weather data to be modified.
            - dry_bulb_temperature: dry bulb temperature.
        :param value: timeseries containing new weather data to be set with units.
        """
        if value is not None:
            start_date = self._timestamps[0]
            new_start_date = value.index[0]
            if new_start_date < start_date:
                raise WeatherDataOutOfBoundsError(message="New " + key + " starts at "
                                                          + new_start_date.strftime('%Y-%m-%m %H:%M:%S')
                                                          + " and it should be later than "
                                                          + start_date.strftime('%Y-%m-%m %H:%M:%S'))
            end_date = self._timestamps[-1]
            new_end_date = value.index[-1]
            if new_end_date > end_date:
                raise WeatherDataOutOfBoundsError(message="New " + key + " starts at "
                                                          + new_end_date.strftime('%Y-%m-%m %H:%M:%S')
                                                          + " and it should be sooner than "
                                                          + end_date.strftime('%Y-%m-%m %H:%M:%S'))
            indexes_to_set = (self._timestamps >= new_start_date) & (self._timestamps <= new_end_date)
            timestamps_to_set = self._timestamps[indexes_to_set].astype('int64') / 10**9
            timestamps_to_interp = value.index.astype('int64') / 10**9
            if key == 'dry_bulb_temperature':
                new_values = np.interp(timestamps_to_set, timestamps_to_interp, value.data.to(ureg.degC).m) * ureg.degC
                if self._dry_bulb_temperature is None:
                    self._dry_bulb_temperature = new_values
                else:
                    self._dry_bulb_temperature[indexes_to_set] = new_values
            elif key == 'dew_point_temperature':
                new_values = np.interp(timestamps_to_set, timestamps_to_interp, value.data.to(ureg.degC).m) * ureg.degC
                if self._dew_point_temperature is None:
                    self._dew_point_temperature = new_values
                else:
                    self._dew_point_temperature[indexes_to_set] = new_values
            elif key == 'relative_humidity':
                new_values = np.interp(timestamps_to_set, timestamps_to_interp, value.data.m if value.data.dimensionality  == ureg.percent.dimensionality else value.data.m * 100.0) * ureg.percent
                if self._relative_humidity is None:
                    self._relative_humidity = new_values
                else:
                    self._relative_humidity[indexes_to_set] = new_values
            elif key == 'specific_humidity':
                new_values = np.interp(timestamps_to_set, timestamps_to_interp, value.data.to(ureg.gram/ureg.kilogram).m) * (ureg.gram/ureg.kilogram)
                if self._specific_humidity is None:
                    self._specific_humidity = new_values
                else:
                    self._specific_humidity[indexes_to_set] = new_values
            elif key == 'atmospheric_station_pressure':
                new_values = np.interp(timestamps_to_set, timestamps_to_interp, value.data.to(ureg.Pa).m) * ureg.Pa
                if self._atmospheric_station_pressure is None:
                    self._atmospheric_station_pressure = new_values
                else:
                    self._atmospheric_station_pressure[indexes_to_set] = new_values
            elif key == 'extraterrestrial_horizontal_radiation':
                new_values = np.interp(timestamps_to_set, timestamps_to_interp, value.data.to(ureg.watt/(ureg.meter ** 2)).m) * (ureg.watt/(ureg.meter ** 2))
                if self._extraterrestrial_horizontal_radiation is None:
                    self._extraterrestrial_horizontal_radiation = new_values
                else:
                    self._extraterrestrial_horizontal_radiation[indexes_to_set] = new_values
            elif key == 'extraterrestrial_direct_normal_radiation':
                new_values = np.interp(timestamps_to_set, timestamps_to_interp, value.data.to(ureg.watt / (ureg.meter ** 2)).m) * (ureg.watt / (ureg.meter ** 2))
                if self._extraterrestrial_direct_normal_radiation is None:
                    self._extraterrestrial_direct_normal_radiation = new_values
                else:
                    self._extraterrestrial_direct_normal_radiation[indexes_to_set] = new_values
            elif key == 'horizontal_infrared_radiation_intensity':
                new_values = np.interp(timestamps_to_set, timestamps_to_interp, value.data.to(ureg.watt / (ureg.meter ** 2)).m) * (ureg.watt / (ureg.meter ** 2))
                if self._horizontal_infrared_radiation_intensity is None:
                    self._horizontal_infrared_radiation_intensity = new_values
                else:
                    self._horizontal_infrared_radiation_intensity[indexes_to_set] = new_values
            elif key == 'global_horizontal_radiation':
                new_values = np.interp(timestamps_to_set, timestamps_to_interp, value.data.to(ureg.watt / (ureg.meter ** 2)).m) * (ureg.watt / (ureg.meter ** 2))
                if self._global_horizontal_radiation is None:
                    self._global_horizontal_radiation = new_values
                else:
                    self._global_horizontal_radiation[indexes_to_set] = new_values
            elif key =='direct_normal_radiation':
                new_values = np.interp(timestamps_to_set, timestamps_to_interp, value.data.to(ureg.watt / (ureg.meter ** 2)).m) * (ureg.watt / (ureg.meter ** 2))
                if self._direct_normal_radiation is None:
                    self._direct_normal_radiation = new_values
                else:
                    self._direct_normal_radiation[indexes_to_set] = new_values
            elif key == 'diffuse_horizontal_radiation':
                new_values = np.interp(timestamps_to_set, timestamps_to_interp, value.data.to(ureg.watt / (ureg.meter ** 2)).m) * (ureg.watt / (ureg.meter ** 2))
                if self._diffuse_horizontal_radiation is None:
                    self._diffuse_horizontal_radiation = new_values
                else:
                    self._diffuse_horizontal_radiation[indexes_to_set] = new_values
            elif key == 'global_horizontal_illuminance':
                new_values = np.interp(timestamps_to_set, timestamps_to_interp, value.data.to(ureg.lumen / (ureg.meter ** 2)).m) * (ureg.lumen / (ureg.meter ** 2))
                if self._global_horizontal_illuminance is None:
                    self._global_horizontal_illuminance = new_values
                else:
                    self._global_horizontal_illuminance[indexes_to_set] = new_values
            elif key == 'direct_normal_illuminance':
                new_values = np.interp(timestamps_to_set, timestamps_to_interp, value.data.to(ureg.lumen / (ureg.meter ** 2)).m) * (ureg.lumen / (ureg.meter ** 2))
                if self._direct_normal_illuminance is None:
                    self._direct_normal_illuminance = new_values
                else:
                    self._direct_normal_illuminance[indexes_to_set] = new_values
            elif key == 'diffuse_horizontal_illuminance':
                new_values = np.interp(timestamps_to_set, timestamps_to_interp, value.data.to(ureg.lumen / (ureg.meter ** 2)).m) * (ureg.lumen / (ureg.meter ** 2))
                if self._diffuse_horizontal_illuminance is None:
                    self._diffuse_horizontal_illuminance = new_values
                else:
                    self._diffuse_horizontal_illuminance[indexes_to_set] = new_values
            elif key == 'zenith_illuminance':
                new_values = np.interp(timestamps_to_set, timestamps_to_interp, value.data.to(ureg.candela / (ureg.meter ** 2)).m) * (ureg.candela / (ureg.meter ** 2))
                if self._zenith_illuminance is None:
                    self._zenith_illuminance = new_values
                else:
                    self._zenith_illuminance[indexes_to_set] = new_values
            elif key == 'wind_direction':
                new_values = np.interp(timestamps_to_set, timestamps_to_interp, value.data.m if value.data.dimensionality == ureg.degree.dimensionality else np.rad2deg(value.data.m)) * ureg.degree
                if self._wind_direction is None:
                    self._wind_direction = new_values
                else:
                    self._wind_direction[indexes_to_set] = new_values
            elif key == 'wind_speed':
                new_values = np.interp(timestamps_to_set, timestamps_to_interp, value.data.to(ureg.meter / ureg.second).m) * (ureg.meter / ureg.second)
                if self._wind_speed is None:
                    self._wind_speed = new_values
                else:
                    self._wind_speed[indexes_to_set] = new_values
            elif key == 'total_sky_cover':
                new_values = np.interp(timestamps_to_set, timestamps_to_interp, value.data.m) * ureg.tenth
                if self._total_sky_cover is None:
                    self._total_sky_cover = new_values
                else:
                    self._total_sky_cover[indexes_to_set] = new_values
            elif key == 'opaque_sky_cover':
                new_values = np.interp(timestamps_to_set, timestamps_to_interp, value.data.m) * ureg.tenth
                if self._opaque_sky_cover is None:
                    self._opaque_sky_cover = new_values
                else:
                    self._opaque_sky_cover[indexes_to_set] = new_values
            elif key == 'visibility':
                new_values = np.interp(timestamps_to_set, timestamps_to_interp, value.data.to(ureg.kilometer).m) * ureg.kilometer
                if self._visibility is None:
                    self._visibility = new_values
                else:
                    self._visibility[indexes_to_set] = new_values
            elif key == 'ceiling_height':
                new_values = np.interp(timestamps_to_set, timestamps_to_interp, value.data.to(ureg.meter).m) * ureg.meter
                if self._ceiling_height is None:
                    self._ceiling_height = new_values
                else:
                    self._ceiling_height[indexes_to_set] = new_values
            elif key == 'precipitable_water':
                new_values = np.interp(timestamps_to_set, timestamps_to_interp, value.data.to(ureg.centimeter).m) * ureg.centimeter
                if self._precipitable_water is None:
                    self._precipitable_water = new_values
                else:
                    self._precipitable_water[indexes_to_set] = new_values
            elif key == 'aerosol_optical_depth':
                new_values = np.interp(timestamps_to_set, timestamps_to_interp, value.data.m) * ureg.dimensionless
                if self._aerosol_optical_depth is None:
                    self._aerosol_optical_depth = new_values
                else:
                    self._aerosol_optical_depth[indexes_to_set] = new_values
            elif key == 'snow_depth':
                new_values = np.interp(timestamps_to_set, timestamps_to_interp, value.data.to(ureg.centimeter).m) * ureg.centimeter
                if self._snow_depth is None:
                    self._snow_depth = new_values
                else:
                    self._snow_depth[indexes_to_set] = new_values
            elif key == 'days_since_last_snowfall':
                new_values = np.interp(timestamps_to_set, timestamps_to_interp, value.data.m) * ureg.dimensionless
                if self._days_since_last_snowfall is None:
                    self._days_since_last_snowfall = new_values
                else:
                    self._days_since_last_snowfall[indexes_to_set] = new_values
            elif key == 'albedo':
                new_values = np.interp(timestamps_to_set, timestamps_to_interp, value.data.m) * ureg.dimensionless
                if self._albedo is None:
                    self._albedo = new_values
                else:
                    self._albedo[indexes_to_set] = new_values
            elif key == 'liquid_precipitation_depth':
                new_values = np.interp(timestamps_to_set, timestamps_to_interp, value.data.to(ureg.millimeter).m) * ureg.millimeter
                if self._liquid_precipitation_depth is None:
                    self._liquid_precipitation_depth = new_values
                else:
                    self._liquid_precipitation_depth[indexes_to_set] = new_values
            elif key == 'liquid_precipitation_quantity':
                new_values = np.interp(timestamps_to_set, timestamps_to_interp, value.data.to(ureg.hour).m) * ureg.hour
                if self._liquid_precipitation_quantity is None:
                    self._liquid_precipitation_quantity = new_values
                else:
                    self._liquid_precipitation_quantity[indexes_to_set] = new_values
            elif key == 'zenith_angle_sun':
                new_values = np.interp(timestamps_to_set, timestamps_to_interp, value.data.m if value.data.dimensionality == ureg.degree.dimensionality else np.rad2deg(value.data.m)) * ureg.degree
                if self._zenith_angle_sun is None:
                    self._zenith_angle_sun = new_values
                else:
                    self._zenith_angle_sun[indexes_to_set] = new_values
            elif key == 'azimuth_angle_sun':
                new_values = np.interp(timestamps_to_set, timestamps_to_interp, value.data.m if value.data.dimensionality == ureg.degree.dimensionality else np.rad2deg(value.data.m)) * ureg.degree
                if self._azimuth_angle_sun is None:
                    self._azimuth_angle_sun = new_values
                else:
                    self._azimuth_angle_sun[indexes_to_set] = new_values
            elif key == 'sky_temperature':
                new_values = np.interp(timestamps_to_set, timestamps_to_interp, value.data.to(ureg.degC).m) * ureg.degC
                if self._sky_temperature is None:
                    self._sky_temperature = new_values
                else:
                    self._sky_temperature[indexes_to_set] = new_values
            else:
                raise WeatherDataUnknownItemError(message='Weather data ' + key + ' are unknown.')

    @abstractmethod
    def save(self, file_name, out_dir='.'):
        """
        Save weather data.
        :param file_name: file name where weather data must be saved
        :param out_dir: output directory where weather data must be saved
        """
        pass

class EnergyPlusWeatherData(WeatherData):
    """
    Class representing EnergyPlus weather data.

    Attributes:
        country: country in which weather data were collected.
        state: state (if any) in which weather data were collected.
        city: city in which weather data were collected.
        data_type: type of weather data being collected (e.g. TMY1, TMY2, TMY3, etc ...)
        WMO_code: WMO code of weather data
        latitude: latitude at which weather data were collected.
        longitude: longitude at which weather data were collected.
        utc: UTC time at which weather data were collected.
        altitude: altitude at which weather data were collected (in meter)
        source_design_conditions: source of design conditions of the period during which weather data were collected.
        design_conditions: design conditions of the period during which weather data were collected.
        extreme_periods: extreme periods during which weather data were collected.
        ground_layers: ground layers of the location at which weather data were collected.
        is_leap_year: True if weather data were collected during a leap year.
        daylight_saving_start_day: start day of daylight saving.
        daylight_saving_end_day: end day of daylight saving.
        holidays: holidays over the period during which weather data were collected.
    """

    class DesignCondition():
        """
        Class representing a design condition as stated in an EPW file.

        Attributes:
            source_name (str): source name of the design condition
            values: values of the design condition
        """
        def __init__(self, source_name, heating = [], cooling = [], extremes = []):
            """
            :param name: name of the design condition
            :param heating: heating conditions
            :param cooling: cooling conditions
            :param extremes: extremes conditions
            """
            self.source_name = source_name
            self.heating = heating
            self.cooling = cooling
            self.extremes = extremes

    class ExtremePeriod():
        """
        Class representing an extreme period as stated in an EPW file.

        Attributs:
            name: name of the extreme period.
            type: type of the extreme period.
            start: start date of the extreme period.
            end: end date of the extreme period.
        """
        def __init__(self, name, type='Extreme', start=None, end=None):
            """
            :param name: name of the the extreme period.
            :param type: type of the extreme period
            :param start: start date of the extreme  period
            :param end: end date of the extreme period.
            """
            self.name = name
            self.type = type
            self.start = start
            self.end = end

    class GroundLayer():
        """
        Class representing a ground layer as defined in an EPW file.

        Attributs:
            depth: depth of the ground layer (in meter)
            conductivity: thermal conductivity of the ground layer (in Watts per squared meter and Kelvin)
            density: density of the ground layer (in kilograms per cubic meter)
            specific_heat: specific heat capacity of the ground layer (in Joules per kilogram)
            average_monthly_temperature: average temperature of the ground layer for every month of the year (in degrees Celsius)
        """
        def __init__(self, depth = None, conductivity = None, density = None, specific_heat = None, average_monthly_temperature = []):
            """
            :param depth: depth of the ground layer (in meter)
            :param conductivity: thermal conductivity of the ground layer (in Watts per squared meter and Kelvin)
            :param density: density of the ground layer (in kilograms per cubic meter)
            :param specific_heat: specific heat capacity of the ground layer (in Joules per kilogram)
            :param average_monthly_temperature: average temperature of the ground layer for every month of the year (in degrees Celsius)
            """
            self.depth = depth
            self.conductivity = conductivity
            self.density = density
            self.specific_heat = specific_heat
            self.average_monthly_temperature = average_monthly_temperature

    def __init__(self, timestamps, country = '', state = '-', city = '', data_type = '',
                 WMO_code = '', latitude = 0.0, longitude = 0.0, utc = 0.0,
                 altitude = 0.0 * ureg.meter, source_design_conditions = '',
                 design_conditions = [], extreme_periods = [], ground_layers = [],
                 is_leap_year = False, daylight_saving_start_day = 0, daylight_saving_end_day = 0,
                 holidays = [], comment_1 = '', comment_2 = ''):
        """
        :param timestamps: list of timestamps at which weather data were collected.
        :param country: country in which weather data were collected.
        :param state: state (if any) in which weather data were collected.
        :param city: city in which weather data were collected.
        :param data_type: type of weather data being collected (e.g. TMY1, TMY2, TMY3, etc ...)
        :param WMO_code: WMO code of weather data
        :param latitude: latitude at which weather data were collected.
        :param longitude: longitude at which weather data were collected.
        :param utc: UTC time at which weather data were collected.
        :param altitude: altitude at which weather data were collected (in meter)
        :param source_design_conditions: source of design conditions of the period during which weather data were collected.
        :param design_conditions: design conditions of the period during which weather data were collected.
        :param extreme_periods: extreme periods during which weather data were collected.
        :param ground_layers: ground layers of the location at which weather data were collected.
        :param is_leap_year: True if weather data were collected during a leap year.
        :param daylight_saving_start_day: start day of daylight saving.
        :param daylight_saving_end_day: end day of daylight saving.
        :param holidays: holidays over the period during which weather data were collected.
        """
        WeatherData.__init__(self, timestamps)
        self.country = country
        self.state = state
        self.city = city
        self.data_type = data_type
        self.WMO_code = WMO_code
        self.latitude = latitude
        self.longitude = longitude
        self.utc = utc
        self.altitude = altitude
        self.design_conditions = design_conditions
        self.extreme_periods = extreme_periods
        self.ground_layers = ground_layers
        self.is_leap_year = is_leap_year
        self.daylight_saving_start_day = daylight_saving_start_day
        self.daylight_saving_end_day = daylight_saving_end_day
        self.holidays = holidays
        self.comment_1 = comment_1
        self.comment_2 = comment_2
        self.data_source_uncertainty = None
        self.present_weather_observation = None
        self.present_weather_codes = None


    def save(self, file_name, out_dir='.'):
        """
        Save weather data.
        :param file_name: file name where weather data must be saved
        :param out_dir: output directory where weather data must be saved
        """
        YEARS = [y - 1 if (self._timestamps.month[n] == 1) & (self._timestamps.day[n] == 1) & (self._timestamps.hour[n] == 0) else y for n, y in enumerate(self._timestamps.year)]
        MONTHS = [(m - 1) + 12 * ((m - 1) == 0) if (self._timestamps.day[n] == 1) & (self._timestamps.hour[n] == 0) else m for n, m in enumerate(self._timestamps.month)]
        DAYS = [(d - 1) + self._timestamps.day[n - 1] * ((d - 1) == 0) if (self._timestamps[n].hour == 0) else d for n, d in enumerate(self._timestamps.day)]
        HOURS = [24 if (h == 0) else h for h in self._timestamps.hour]
        dt = self._timestamps[1] - self._timestamps[0]
        NUM_RECORDS_PER_HOUR = int(3600.0 / dt.total_seconds())
        DAY_OF_WEEK = self._timestamps[0].strftime("%A")
        with open(os.path.join(out_dir, file_name), 'w') as file:
            file.write(f"LOCATION,{self.city},{self.state},{self.country},{self.data_type},{self.WMO_code},{str(self.latitude)},{str(self.longitude)},{str(self.utc)},{str(self.altitude)}\n")
            design_conditions_str = f"DESIGN CONDITIONS,{str(len(self.design_conditions))},"
            for dc in self.design_conditions:
                design_conditions_str += dc.source_name + ",,Heating," + ",".join(str(v) for v in dc.heating)
                design_conditions_str += ",Cooling," + ",".join(str(v) for v in dc.cooling)
                design_conditions_str += ",Extremes," + ",".join(str(v) for v in dc.extremes)
            file.write(design_conditions_str + "\n")
            extreme_periods_str = f"TYPICAL/EXTREME PERIODS,{str(len(self.extreme_periods))}"
            for ep in self.extreme_periods:
                extreme_periods_str += "," + ep.name + "," + ep.type + "," + str(ep.start.month) + "/" + str(ep.start.day) + "," + str(ep.end.month) + "/" + str(ep.end.day)
            file.write(extreme_periods_str + "\n")
            ground_temperatures_str = f"GROUND TEMPERATURES,{str(len(self.ground_layers))}"
            for gl in self.ground_layers:
                conductivity_str = '' if gl.conductivity is None else str(gl.conductivity)
                density_str = '' if gl.density is None else str(gl.density)
                specific_heat_str = '' if gl.specific_heat is None else str(gl.specific_heat)
                ground_temperatures_str += "," + str(gl.depth) + "," + conductivity_str + "," + density_str + "," + specific_heat_str + "," + ",".join(str(v) for v in gl.average_monthly_temperature)
            file.write(ground_temperatures_str + "\n")
            leap_str = "Yes" if self.is_leap_year else "No"
            file.write(f"HOLIDAYS/DAYLIGHT SAVINGS,{leap_str},{self.daylight_saving_start_day},{self.daylight_saving_end_day},{str(len(self.holidays))}\n")
            file.write(f"COMMENTS 1,{self.comment_1}\n")
            file.write(f"COMMENTS 2,{self.comment_2}\n")
            start_str = str(MONTHS[0]) + "/" + str(DAYS[0]) + "/" + str(YEARS[0])
            end_str = str(MONTHS[-1]) + "/" + str(DAYS[-1]) + "/" + str(YEARS[-1])
            file.write(f"DATA PERIODS,{str(len(set(YEARS)))},{str(NUM_RECORDS_PER_HOUR)},Data,{DAY_OF_WEEK},{start_str},{end_str}\n")
            df = pd.DataFrame({'Year': YEARS,
                               'Month': MONTHS,
                               'Day': DAYS,
                               'Hour': HOURS,
                               'Minute': self._timestamps.minute.tolist(),
                               'Data Source and Uncertainty Flags': ['?9?9?9?9E0?9?9?9?9?9?9?9?9?9?9?9?9?9?9?9*9*9?9?9?9'] * len(self._timestamps) if self.data_source_uncertainty is None else self.data_source_uncertainty,
                               'Dry Bulb Temperature': [99.9] * len(self._timestamps) if self._dry_bulb_temperature is None else self._dry_bulb_temperature.m.tolist(),
                               'Dew Point Temperature': [99.9] * len(self._timestamps) if self._dew_point_temperature is None else self._dew_point_temperature.m.tolist(),
                               'Relative Humidity': [999] * len(self._timestamps) if self._relative_humidity is None else self._relative_humidity.m.tolist(),
                               'Atmospheric Station Pressure': [999999] * len(self._timestamps) if self._atmospheric_station_pressure is None else self._atmospheric_station_pressure.m.tolist(),
                               'Extraterrestrial Horizontal Radiation': [9999] * len(self._timestamps) if self._extraterrestrial_horizontal_radiation is None else self._extraterrestrial_horizontal_radiation.m.tolist(),
                               'Extraterrestrial Direct Normal Radiation': [9999] * len(self._timestamps) if self._extraterrestrial_direct_normal_radiation is None else self._extraterrestrial_direct_normal_radiation.m.tolist(),
                               'Horizontal Infrared Radiation Intensity': [9999] * len(self._timestamps) if self._horizontal_infrared_radiation_intensity is None else self._horizontal_infrared_radiation_intensity.m.tolist(),
                               'Global Horizontal Radiation': [9999] * len(self._timestamps) if self._global_horizontal_radiation is None else self._global_horizontal_radiation.m.tolist(),
                               'Direct Normal Radiation': [9999] * len(self._timestamps) if self._direct_normal_radiation is None else self._direct_normal_radiation.m.tolist(),
                               'Diffuse Horizontal Radiation': [9999] * len(self._timestamps) if self._diffuse_horizontal_radiation is None else self._diffuse_horizontal_radiation.m.tolist(),
                               'Global Horizontal Illuminance': [999999] * len(self._timestamps) if self._global_horizontal_illuminance is None else self._global_horizontal_illuminance.m.tolist(),
                               'Direct Normal Illuminance': [999999] * len(self._timestamps) if self._direct_normal_illuminance is None else self._direct_normal_illuminance.m.tolist(),
                               'Diffuse Horizontal Illuminance': [999999] * len(self._timestamps) if self._diffuse_horizontal_illuminance is None else self._diffuse_horizontal_illuminance.m.tolist(),
                               'Zenith Illuminance': [9999] * len(self._timestamps) if self._zenith_illuminance is None else self._zenith_illuminance.m.tolist(),
                               'Wind Direction': [999] * len(self._timestamps) if self._wind_direction is None else self._wind_direction.m.tolist(),
                               'Wind Speed': [999] * len(self._timestamps) if self._wind_speed is None else self._wind_speed.m.tolist(),
                               'Total Sky Cover': [99] * len(self._timestamps) if self._total_sky_cover is None else self._total_sky_cover.m.tolist(),
                               'Opaque Sky Cover': [99] * len(self._timestamps) if self._opaque_sky_cover is None else self._opaque_sky_cover.m.tolist(),
                               'Visibility': [9999] * len(self._timestamps) if self._visibility is None else self._visibility.m.tolist(),
                               'Ceiling Height': [99999] * len(self._timestamps) if self._ceiling_height is None else self._ceiling_height.m.tolist(),
                               'Present Weather Observation': [77777] * len(self._timestamps) if self.present_weather_observation is None else self.present_weather_observation.values.tolist(),
                               'Present Weather Codes': [9] * len(self._timestamps) if self.present_weather_codes is None else self.present_weather_codes.values.tolist(),
                               'Precipitable Water': [999] * len(self._timestamps) if self._precipitable_water is None else self._precipitable_water.m.tolist(),
                               'Aerosol Optical Depth': [0.999] * len(self._timestamps) if self._aerosol_optical_depth is None else self._aerosol_optical_depth.m.tolist(),
                               'Snow Depth': [999] * len(self._timestamps) if self._snow_depth is None else self._snow_depth.m.tolist(),
                               'Days Since Last Snowfall': [99] * len(self._timestamps) if self._days_since_last_snowfall is None else self._days_since_last_snowfall.m.tolist(),
                               'Albedo': [999] * len(self._timestamps) if self._albedo is None else self._albedo.m.tolist(),
                               'Liquid Precipitation Depth': [999] * len(self._timestamps) if self._liquid_precipitation_depth is None else self._liquid_precipitation_depth.m.tolist(),
                               'Liquid Precipitation Quantity': [99] * len(self._timestamps) if self._liquid_precipitation_quantity is None else self._liquid_precipitation_quantity.m.tolist()})
            df.to_csv(file, header=False, index=False, lineterminator='\n')

class CSVWeatherData(WeatherData):
    """
    Class containing weather data extracted from CSV file.
    """

    def __init__(self, timestamps, mapping={}, date_format = '%Y-%m-%d %H:%M:%S'):
        """
        :param timestamps: list of timestamps at which weather data were collected.
        :param mapping: dictionary containing the meaning of each column and the units of their corresponding quantities.
        """
        WeatherData.__init__(self, timestamps)
        self.mapping = mapping
        self.date_format = date_format

    def save(self, file_name, out_dir='.'):
        """
        Save weather data.
        :param file_name: file name where weather data must be saved
        :param out_dir: output directory where weather data must be saved
        """
        df = pd.DataFrame({self.mapping['timestamps']: self._timestamps})
        for k in self.keys():
            df[self.mapping[k]] = self[k].values.tolist()
        df = df.set_index(self.mapping['timestamps'])
        df.to_csv(os.path.join(out_dir, file_name), index=True, date_format=self.date_format)

class WeatherDataLoader():
    """
    Class to load weather data.

    Attributes:
        weather_file: file containing weather data.
    """
    __metaclass__ = ABCMeta

    def __init__(self, weather_file):
        """
        :param weather_file: file containg weather data.
        """
        self.weather_file = weather_file

    def load(self):
        weather_data = self.get_instance()
        weather_data['dry_bulb_temperature'] = self.get_dry_bulb_temperature()
        weather_data['dew_point_temperature'] = self.get_dew_point_temperature()
        weather_data['relative_humidity'] = self.get_relative_humidity()
        weather_data['specific_humidity'] = self.get_specific_humidity()
        weather_data['atmospheric_station_pressure'] = self.get_atmospheric_station_pressure()
        weather_data['extraterrestrial_horizontal_radiation'] = self.get_extraterrestrial_horizontal_radiation()
        weather_data['extraterrestrial_direct_normal_radiation'] = self.get_extraterrestrial_direct_normal_radiation()
        weather_data['horizontal_infrared_radiation_intensity'] = self.get_horizontal_infrared_radiation_intensity()
        weather_data['global_horizontal_radiation'] = self.get_global_horizontal_radiation()
        weather_data['direct_normal_radiation'] = self.get_direct_normal_radiation()
        weather_data['diffuse_horizontal_radiation'] = self.get_diffuse_horizontal_radiation()
        weather_data['global_horizontal_illuminance'] = self.get_global_horizontal_illuminance()
        weather_data['direct_normal_illuminance'] = self.get_direct_normal_illuminance()
        weather_data['diffuse_horizontal_illuminance'] = self.get_diffuse_horizontal_illuminance()
        weather_data['zenith_illuminance'] = self.get_zenith_illuminance()
        weather_data['wind_direction'] = self.get_wind_direction()
        weather_data['wind_speed'] = self.get_wind_speed()
        weather_data['total_sky_cover'] = self.get_total_sky_cover()
        weather_data['opaque_sky_cover'] = self.get_opaque_sky_cover()
        weather_data['visibility'] = self.get_visibility()
        weather_data['ceiling_height'] = self.get_ceiling_height()
        weather_data['aerosol_optical_depth'] = self.get_aerosol_optical_depth()
        weather_data['precipitable_water'] = self.get_precipitable_water()
        weather_data['aerosol_optical_depth'] = self.get_aerosol_optical_depth()
        weather_data['snow_depth'] = self.get_snow_depth()
        weather_data['days_since_last_snowfall'] = self.get_days_since_last_snowfall()
        weather_data['albedo'] = self.get_albedo()
        weather_data['liquid_precipitation_depth'] = self.get_liquid_precipitation_depth()
        weather_data['liquid_precipitation_quantity'] = self.get_liquid_precipitation_quantity()
        weather_data['zenith_angle_sun'] = self.get_zenith_angle_sun()
        weather_data['azimuth_angle_sun'] = self.get_azimuth_angle_sun()
        weather_data['sky_temperature'] = self.get_sky_temperature()
        return weather_data

    @abstractmethod
    def get_instance(self):
        """
        :return: instance of weather data
        """
        pass

    @abstractmethod
    def get_dry_bulb_temperature(self):
        """
        :return: dry bulb temperature
        """
        pass

    @abstractmethod
    def get_dew_point_temperature(self):
        """
        :return: dew point temperature
        """
        pass

    @abstractmethod
    def get_relative_humidity(self):
        """
        :return: relative humidity
        """
        pass

    @abstractmethod
    def get_specific_humidity(self):
        """
        :return: specific humidity
        """
        pass

    @abstractmethod
    def get_atmospheric_station_pressure(self):
        """
        :return: atmospheric station pressure
        """
        pass

    @abstractmethod
    def get_extraterrestrial_horizontal_radiation(self):
        """
        :return: extraterrestrial horizontal radiation
        """
        pass

    @abstractmethod
    def get_extraterrestrial_direct_normal_radiation(self):
        """
        :return: extraterrestrial direct normal radiation
        """
        pass

    @abstractmethod
    def get_horizontal_infrared_radiation_intensity(self):
        """
        :return: horizontal infrared radiation intensity
        """
        pass

    @abstractmethod
    def get_global_horizontal_radiation(self):
        """
        :return: global horizontal radiation
        """
        pass

    @abstractmethod
    def get_direct_normal_radiation(self):
        """
        :return: direct normal radiation
        """
        pass

    @abstractmethod
    def get_diffuse_horizontal_radiation(self):
        """
        :return: diffuse horizontal radiation
        """
        pass

    @abstractmethod
    def get_global_horizontal_illuminance(self):
        """
        :return: global horizontal illuminance
        """
        pass

    @abstractmethod
    def get_direct_normal_illuminance(self):
        """
        :return: direct normal illuminance
        """
        pass

    @abstractmethod
    def get_diffuse_horizontal_illuminance(self):
        """
        :return: diffuse horizontal illuminance
        """
        pass

    @abstractmethod
    def get_zenith_illuminance(self):
        """
        :return: zenith illuminance
        """
        pass

    @abstractmethod
    def get_wind_direction(self):
        """
        :return: wind direction
        """
        pass

    @abstractmethod
    def get_wind_speed(self):
        """
        :return: wind direction
        """
        pass

    @abstractmethod
    def get_total_sky_cover(self):
        """
        :return: total sky cover
        """
        pass

    @abstractmethod
    def get_opaque_sky_cover(self):
        """
        :return: opaque sky cover
        """
        pass

    @abstractmethod
    def get_visibility(self):
        """
        :return: visibility
        """
        pass

    @abstractmethod
    def get_ceiling_height(self):
        """
        :return: ceiling height
        """
        pass

    @abstractmethod
    def get_aerosol_optival_depth(self):
        """
        :return: aerosol optival depth
        """
        pass

    @abstractmethod
    def get_precipitable_water(self):
        """
        :return: precipitable water
        """
        pass

    @abstractmethod
    def get_aerosol_optical_depth(self):
        """
        :return: aerosol optical depth
        """
        pass

    @abstractmethod
    def get_snow_depth(self):
        """
        :return: snow depth
        """
        pass

    @abstractmethod
    def get_days_since_last_snowfall(self):
        """
        :return: days since last snowfall
        """
        pass

    @abstractmethod
    def get_albedo(self):
        """
        :return: albedo
        """
        pass

    @abstractmethod
    def get_liquid_precipitation_depth(self):
        """
        :return: liquid precipitation depth
        """
        pass

    @abstractmethod
    def get_liquid_precipitation_quantity(self):
        """
        :return: liquid precipitation quantity
        """
        pass

    @abstractmethod
    def get_zenith_angle_sun(self):
        """
        :return: zenith angle sun
        """
        pass

    @abstractmethod
    def get_azimuth_angle_sun(self):
        """
        :return: azimuth angle sun
        """
        pass

    @abstractmethod
    def get_sky_temperature(self):
        """
        :return: mean radiant temperature
        """
        pass



class EPWDataLoader(WeatherDataLoader):
    """
    Class to load EPW data.

    Attributes:
        weather_file: file containing EPW data.
    """
    __metaclass__ = ABCMeta

    def __init__(self, weather_file, year=datetime.today().year):
        """
        :param weather_file: file containg EPW data.
        """
        WeatherDataLoader.__init__(self, weather_file)
        self.year = year
        self.latitude = 0.0
        self.longitude = 0.0
        self.utc = 0.0
        self.data = None
        self.timestamps = None

    def load(self):
        weather_data = WeatherDataLoader.load(self)
        weather_data.data_source_uncertainty = self.get_data_source_uncertainty()
        weather_data.present_weather_observation = self.get_present_weather_observation()
        weather_data.present_weather_codes = self.get_present_weather_codes()
        return weather_data

    def get_instance(self):
        """
        :return: instance of weather data
        """
        colnames = ['year', 'month', 'day', 'hour', 'minute', 'data_source_unct',
                    'temp_air', 'temp_dew', 'relative_humidity',
                    'atmospheric_pressure', 'etr', 'etrn', 'ghi_infrared', 'ghi',
                    'dni', 'dhi', 'global_hor_illum', 'direct_normal_illum',
                    'diffuse_horizontal_illum', 'zenith_luminance',
                    'wind_direction', 'wind_speed', 'total_sky_cover',
                    'opaque_sky_cover', 'visibility', 'ceiling_height',
                    'present_weather_observation', 'present_weather_codes',
                    'precipitable_water', 'aerosol_optical_depth', 'snow_depth',
                    'days_since_last_snowfall', 'albedo',
                    'liquid_precipitation_depth', 'liquid_precipitation_quantity']
        self.data = pd.DataFrame(columns=colnames)
        with open(self.weather_file, 'r') as file:
            lines = file.readlines()
        for line in lines:
            fragments = line.split(',')
            if fragments[0] == 'LOCATION':
                city = fragments[1]
                state = fragments[2]
                country = fragments[3]
                data_type = fragments[4]
                WMO_code = int(fragments[5])
                self.latitude = float(fragments[6])
                self.longitude = float(fragments[7])
                self.utc = float(fragments[8])
                altitude = float(fragments[9])
            elif fragments[0] == 'DESIGN CONDITIONS':
                design_conditions = []
                num_design_conditions = int(fragments[1])
                source_name = fragments[2]
                length_design_condition_segment = 66
                for n in range(num_design_conditions):
                    heating_conditions = []
                    for m in range(15):
                        heating_conditions.append(float(fragments[5 + m + n * length_design_condition_segment]))
                    cooling_conditions = []
                    for m in range(32):
                        cooling_conditions.append(float(fragments[21 + m + n * length_design_condition_segment]))
                    extremes_conditions = []
                    for m in range(16):
                        extremes_conditions.append(float(fragments[54 + m + n * length_design_condition_segment]))
                    design_conditions.append(EnergyPlusWeatherData.DesignCondition(source_name, heating = heating_conditions, cooling = cooling_conditions, extremes = extremes_conditions))
            elif fragments[0] == 'TYPICAL/EXTREME PERIODS':
                extreme_periods = []
                num_extreme_periods = int(fragments[1])
                num_fields_extreme_periods = 4
                for n in range(num_extreme_periods):
                    name = fragments[2 + n * num_fields_extreme_periods]
                    type = fragments[3 + n * num_fields_extreme_periods]
                    start = datetime.strptime(fragments[4 + n * num_fields_extreme_periods].strip(), '%m/%d')
                    end = datetime.strptime(fragments[5 + n * num_fields_extreme_periods].strip(), '%m/%d')
                    extreme_periods.append(EnergyPlusWeatherData.ExtremePeriod(name, type=type, start=start, end=end))
            elif fragments[0] == 'GROUND TEMPERATURES':
                ground_layers = []
                num_ground_layers = int(fragments[1])
                num_fields_ground_layer = 16
                for n in range(num_ground_layers):
                    depth = float(fragments[2 + n * num_fields_ground_layer])
                    conductivity_str = fragments[3 + n * num_fields_ground_layer]
                    conductivity = None if conductivity_str == '' else float(conductivity_str)
                    density_str = fragments[4 + n * num_fields_ground_layer]
                    density = None if density_str == '' else float(density_str)
                    specific_heat_str = fragments[5 + n * num_fields_ground_layer]
                    specific_heat = None if specific_heat_str == '' else float(specific_heat_str)
                    average_monthly_temperature = []
                    for m in range(12):
                        average_monthly_temperature.append(float(fragments[6 + m + n * num_fields_ground_layer]))
                    ground_layers.append(EnergyPlusWeatherData.GroundLayer(depth=depth, conductivity=conductivity, density=density, specific_heat=specific_heat,
                                     average_monthly_temperature=average_monthly_temperature))
            elif fragments[0] == 'HOLIDAYS/DAYLIGHT SAVINGS':
                is_leap_year = False if fragments[1] == 'No' else True
                daylight_saving_start_day = int(fragments[2])
                daylight_saving_end_day = int(fragments[3])
            elif fragments[0] == 'COMMENTS 1':
                comment_1 = fragments[1].replace("\n", "")
            elif fragments[0] == 'COMMENTS 2':
                comment_2 = fragments[1].replace("\n", "")
            elif fragments[0] == 'DATA PERIODS':
                pass
            else:
                self.data = self.data._append({colnames[0]: int(fragments[0]),
                                  colnames[1]: int(fragments[1]),
                                  colnames[2]: int(fragments[2]),
                                  colnames[3]: int(fragments[3]),
                                  colnames[4]: int(fragments[4]),
                                  colnames[5]: fragments[3],
                                  colnames[6]: float(fragments[6]),
                                  colnames[7]: float(fragments[7]),
                                  colnames[8]: float(fragments[8]),
                                  colnames[9]: float(fragments[9]),
                                  colnames[10]: float(fragments[10]),
                                  colnames[11]: float(fragments[11]),
                                  colnames[12]: float(fragments[12]),
                                  colnames[13]: float(fragments[13]),
                                  colnames[14]: float(fragments[14]),
                                  colnames[15]: float(fragments[15]),
                                  colnames[16]: float(fragments[16]),
                                  colnames[17]: float(fragments[17]),
                                  colnames[18]: float(fragments[18]),
                                  colnames[19]: float(fragments[19]),
                                  colnames[20]: float(fragments[20]),
                                  colnames[21]: float(fragments[21]),
                                  colnames[22]: float(fragments[22]),
                                  colnames[23]: float(fragments[23]),
                                  colnames[24]: float(fragments[24]),
                                  colnames[25]: float(fragments[25]),
                                  colnames[26]: int(fragments[26]),
                                  colnames[27]: int(fragments[27]),
                                  colnames[28]: float(fragments[28]),
                                  colnames[29]: float(fragments[29]),
                                  colnames[30]: float(fragments[30]),
                                  colnames[31]: float(fragments[31]),
                                  colnames[32]: float(fragments[32]),
                                  colnames[33]: float(fragments[33]),
                                  colnames[34]: float(fragments[34])}, ignore_index=True)
        self.data["year"] = self.year
        dts = self.data[['month', 'day']].astype(str).apply(lambda x: x.str.zfill(2))
        hrs = (self.data['hour'] - 1).astype(str).str.zfill(2)
        dtscat = self.data['year'].astype(str) + dts['month'] + dts['day'] + hrs
        idx = pd.to_datetime(dtscat.values.tolist(), format='%Y%m%d%H')
        self.timestamps = idx.tz_localize(int(self.utc * 3600)) + timedelta(hours=1)
        self.data.index = self.timestamps
        return EnergyPlusWeatherData(self.timestamps, city=city, state=state, country=country, data_type=data_type,
                                     WMO_code=WMO_code, latitude=self.latitude, longitude=self.longitude, utc=self.utc,
                                     altitude=altitude, design_conditions=design_conditions,
                                     extreme_periods=extreme_periods, ground_layers=ground_layers,
                                     is_leap_year=is_leap_year, daylight_saving_start_day=daylight_saving_start_day,
                                     daylight_saving_end_day=daylight_saving_end_day, comment_1=comment_1,
                                     comment_2=comment_2)

    def get_data_source_uncertainty(self):
        """
        :return: data source uncertainty
        """
        return self.data.data_source_unct

    def get_dry_bulb_temperature(self):
        """
        :return: dry bulb temperature
        """
        return QSeries(index=self.timestamps, data=self.data.temp_air.values * ureg.degC)

    def get_dew_point_temperature(self):
        """
        :return: dew point temperature
        """
        return QSeries(index=self.timestamps, data=self.data.temp_dew.values * ureg.degC)

    def get_relative_humidity(self):
        """
        :return: relative humidity
        """
        return QSeries(index=self.timestamps, data=self.data.relative_humidity.values * ureg.percent)

    def get_specific_humidity(self):
        """
        :return: the outdoor air specific humidity
        """
        sh = specific_humidity(temperature=self.get_dry_bulb_temperature().data,
                               relative_humidity=self.get_relative_humidity().data,
                               pressure=self.get_atmospheric_station_pressure().data)
        return QSeries(index=self.timestamps, data=sh)

    def get_atmospheric_station_pressure(self):
        """
        :return: atmospheric station pressure
        """
        return QSeries(index=self.timestamps, data=self.data.atmospheric_pressure.values * ureg.Pa)

    def get_extraterrestrial_horizontal_radiation(self):
        """
        :return: extraterrestrial horizontal radiation
        """
        return QSeries(index=self.timestamps, data=self.data.etr.values * (ureg.watt / (ureg.meter ** 2)))

    def get_extraterrestrial_direct_normal_radiation(self):
        """
        :return: extraterrestrial direct normal radiation
        """
        return QSeries(index=self.timestamps, data=self.data.etrn.values * (ureg.watt / (ureg.meter ** 2)))

    def get_horizontal_infrared_radiation_intensity(self):
        """
        :return: horizontal infrared radiation intensity
        """
        return QSeries(index=self.timestamps, data=self.data.ghi_infrared.values * (ureg.watt / (ureg.meter ** 2)))

    def get_global_horizontal_radiation(self):
        """
        :return: global horizontal radiation
        """
        return QSeries(index=self.timestamps, data=self.data.ghi.values * (ureg.watt / (ureg.meter ** 2)))

    def get_direct_normal_radiation(self):
        """
        :return: direct normal radiation
        """
        return QSeries(index=self.timestamps, data=self.data.dni.values * (ureg.watt / (ureg.meter ** 2)))

    def get_diffuse_horizontal_radiation(self):
        """
        :return: diffuse horizontal radiation
        """
        return QSeries(index=self.timestamps, data=self.data.dhi.values * (ureg.watt / (ureg.meter ** 2)))

    def get_global_horizontal_illuminance(self):
        """
        :return: global horizontal illuminance
        """
        return QSeries(index=self.timestamps, data=self.data.global_hor_illum.values * (ureg.lumen / (ureg.meter ** 2)))

    def get_direct_normal_illuminance(self):
        """
        :return: direct normal illuminance
        """
        return QSeries(index=self.timestamps, data=self.data.direct_normal_illum.values * (ureg.lumen / (ureg.meter ** 2)))

    def get_diffuse_horizontal_illuminance(self):
        """
        :return: diffuse horizontal illuminance
        """
        return QSeries(index=self.timestamps, data=self.data.diffuse_horizontal_illum.values * (ureg.lumen / (ureg.meter ** 2)))

    def get_zenith_illuminance(self):
        """
        :return: zenith illuminance
        """
        return QSeries(index=self.timestamps, data=self.data.zenith_luminance.values * (ureg.candela / (ureg.meter ** 2)))

    def get_wind_direction(self):
        """
        :return: wind direction
        """
        return QSeries(index=self.timestamps, data=self.data.wind_direction.values * ureg.degree)

    def get_wind_speed(self):
        """
        :return: wind direction
        """
        return QSeries(index=self.timestamps, data=self.data.wind_direction.values * (ureg.meter / ureg.second))

    def get_total_sky_cover(self):
        """
        :return: total sky cover
        """
        return QSeries(index=self.timestamps, data=self.data.total_sky_cover.values * ureg.tenth)

    def get_opaque_sky_cover(self):
        """
        :return: opaque sky cover
        """
        return QSeries(index=self.timestamps, data=self.data.opaque_sky_cover.values * ureg.tenth)

    def get_visibility(self):
        """
        :return: visibility
        """
        return QSeries(index=self.timestamps, data=self.data.visibility.values * ureg.kilometer)

    def get_ceiling_height(self):
        """
        :return: ceiling height
        """
        return QSeries(index=self.timestamps, data=self.data.ceiling_height.values * ureg.meter)

    def get_present_weather_observation(self):
        """
        :return: present weather observation.
        """
        return pd.Series(index=self.timestamps, data=self.data.present_weather_observation.values)

    def get_present_weather_codes(self):
        """
        :return: present weather codes
        """
        return pd.Series(index=self.timestamps, data=self.data.present_weather_codes.values)

    def get_precipitable_water(self):
        """
        :return: precipitable water
        """
        return QSeries(index=self.timestamps, data=self.data.precipitable_water.values * ureg.centimeter)

    def get_aerosol_optical_depth(self):
        """
        :return: aerosol optical depth
        """
        return QSeries(index=self.timestamps, data=self.data.aerosol_optical_depth.values * ureg.centimeter)

    def get_snow_depth(self):
        """
        :return: snow depth
        """
        return QSeries(index=self.timestamps, data=self.data.snow_depth.values * ureg.centimeter)

    def get_days_since_last_snowfall(self):
        """
        :return: days since last snowfall
        """
        return QSeries(index=self.timestamps, data=self.data.days_since_last_snowfall.values * ureg.dimensionless)

    def get_albedo(self):
        """
        :return: albedo
        """
        return QSeries(index=self.timestamps, data=self.data.albedo.values * ureg.dimensionless)

    def get_liquid_precipitation_depth(self):
        """
        :return: liquid precipitation depth
        """
        return QSeries(index=self.timestamps, data=self.data.liquid_precipitation_depth.values * ureg.millimeter)

    def get_liquid_precipitation_quantity(self):
        """
        :return: liquid precipitation quantity
        """
        return QSeries(index=self.timestamps, data=self.data.liquid_precipitation_quantity.values * ureg.hour)

    def get_zenith_angle_sun(self):
        """
        :return: the zenith angle of the sun (in degrees)
        """
        timezone_offset = self.utc
        site = Location(latitude=self.latitude, longitude=self.longitude, tz=timezone_offset)
        timestamps = self.data.index.tz_convert('Etc/GMT' + f"{-int(timezone_offset):+}")
        start_date = timestamps[0] + timedelta(hours=-timezone_offset)
        end_date = timestamps[-1] + timedelta(hours=-timezone_offset)
        dt = timestamps[1] - timestamps[0]
        index = pd.date_range(start=start_date, end=end_date, freq=dt)
        solpos = site.get_solarposition(index)
        return QSeries(index=self.timestamps, data=solpos['zenith'].values * ureg.degree)

    def get_azimuth_angle_sun(self):
        """
        :return: the azimuth angle of the sun (in degrees)
        """
        timezone_offset = self.utc
        site = Location(latitude=self.latitude, longitude=self.longitude, tz=timezone_offset)
        timestamps = self.data.index.tz_convert('Etc/GMT' + f"{-int(timezone_offset):+}")
        start_date = timestamps[0] + timedelta(hours=-timezone_offset)
        end_date = timestamps[-1] + timedelta(hours=-timezone_offset)
        dt = timestamps[1] - timestamps[0]
        index = pd.date_range(start=start_date, end=end_date, freq=dt)
        solpos = site.get_solarposition(index)
        return QSeries(index=self.timestamps, data=solpos['azimuth'].values * ureg.degree)

    def get_sky_temperature(self):
        """
        :return: the outdoor mean radiant temperature
        """
        return QSeries(index=self.timestamps, data=((self.get_horizontal_infrared_radiation_intensity().values / sigma) ** (1 / 4) - 273.15) * ureg.degC)


class CSVDataLoader(WeatherDataLoader):
    """
    Class to load CSV data.

    Attributes:
        weather_file: file containing CSV data.
    """
    __metaclass__ = ABCMeta

    def __init__(self, weather_file, mapping = {}, date_format = '%Y-%m-%d %H:%M:%S', time_zone = 'GMT'):
        """
        :param weather_file: file containg EPW data.
        """
        WeatherDataLoader.__init__(self, weather_file)
        self.mapping = mapping
        self.date_format = date_format
        self.data = None
        self.timestamps = None
        self.time_zone = time_zone

    def get_instance(self):
        """
        :return: instance of weather data
        """
        self.data = pd.read_csv(self.weather_file, index_col=self.mapping['timestamps'], parse_dates=True, date_format=self.date_format)
        self.timestamps = self.data.index.tz_localize(self.time_zone)
        return CSVWeatherData(timestamps=self.timestamps, mapping=self.mapping, date_format=self.date_format)

    def get_dry_bulb_temperature(self):
        """
        :return: dry bulb temperature
        """
        return None if 'dry_bulb_temperature' not in self.mapping.keys() else QSeries(index=self.timestamps, data=self.data[self.mapping['dry_bulb_temperature'][0]].values * self.mapping['dry_bulb_temperature'][1])

    def get_dew_point_temperature(self):
        """
        :return: dew point temperature
        """
        return None if 'dew_point_temperature' not in self.mapping.keys() else QSeries(index=self.timestamps, data=self.data[self.mapping['dew_point_temperature'][0]].values * self.mapping['dew_point_temperature'][1])

    def get_relative_humidity(self):
        """
        :return: relative humidity
        """
        return None if 'relative_humidity' not in self.mapping.keys() else QSeries(index=self.timestamps, data=self.data[self.mapping['relative_humidity'][0]].values * self.mapping['relative_humidity'][1])

    def get_specific_humidity(self):
        """
        :return: specific humidity
        """
        return None if 'specific_humidity' not in self.mapping.keys() else QSeries(index=self.timestamps, data=self.data[self.mapping['specific_humidity'][0]].values * self.mapping['specific_humidity'][1])

    def get_atmospheric_station_pressure(self):
        """
        :return: atmospheric station pressure
        """
        return None if 'atmospheric_station_pressure' not in self.mapping.keys() else QSeries(index=self.timestamps, data=self.data[self.mapping['atmospheric_station_pressure'][0]].values * self.mapping['atmospheric_station_pressure'][1])

    def get_extraterrestrial_horizontal_radiation(self):
        """
        :return: extraterrestrial horizontal radiation
        """
        return None if 'extraterrestrial_horizontal_radiation' not in self.mapping.keys() else QSeries(index=self.timestamps, data=self.data[self.mapping['extraterrestrial_horizontal_radiation'][0]].values * self.mapping['extraterrestrial_horizontal_radiation'][1])

    def get_extraterrestrial_direct_normal_radiation(self):
        """
        :return: extraterrestrial direct normal radiation
        """
        return None if 'extraterrestrial_direct_normal_radiation' not in self.mapping.keys() else QSeries(index=self.timestamps, data=self.data[self.mapping['extraterrestrial_direct_normal_radiation'][0]].values * self.mapping['extraterrestrial_direct_normal_radiation'][1])

    def get_horizontal_infrared_radiation_intensity(self):
        """
        :return: horizontal infrared radiation intensity
        """
        return None if 'horizontal_infrared_radiation_intensity' not in self.mapping.keys() else QSeries(index=self.timestamps, data=self.data[self.mapping['horizontal_infrared_radiation_intensity'][0]].values * self.mapping['horizontal_infrared_radiation_intensity'][1])

    def get_global_horizontal_radiation(self):
        """
        :return: global horizontal radiation
        """
        return None if 'global_horizontal_radiation' not in self.mapping.keys() else QSeries(index=self.timestamps, data=self.data[self.mapping['global_horizontal_radiation'][0]].values * self.mapping['global_horizontal_radiation'][1])

    def get_direct_normal_radiation(self):
        """
        :return: direct normal radiation
        """
        return None if 'direct_normal_radiation' not in self.mapping.keys() else QSeries(index=self.timestamps, data=self.data[self.mapping['direct_normal_radiation'][0]].values * self.mapping['direct_normal_radiation'][1])

    def get_diffuse_horizontal_radiation(self):
        """
        :return: diffuse horizontal radiation
        """
        return None if 'diffuse_horizontal_radiation' not in self.mapping.keys() else QSeries(index=self.timestamps, data=self.data[self.mapping['diffuse_horizontal_radiation'][0]].values * self.mapping['diffuse_horizontal_radiation'][1])

    def get_global_horizontal_illuminance(self):
        """
        :return: global horizontal illuminance
        """
        return None if 'global_horizontal_illuminance' not in self.mapping.keys() else QSeries(index=self.timestamps, data=self.data[self.mapping['global_horizontal_illuminance'][0]].values * self.mapping['global_horizontal_illuminance'][1])

    def get_direct_normal_illuminance(self):
        """
        :return: direct normal illuminance
        """
        return None if 'direct_normal_illuminance' not in self.mapping.keys() else QSeries(index=self.timestamps, data=self.data[self.mapping['direct_normal_illuminance'][0]].values * self.mapping['direct_normal_illuminance'][1])

    def get_diffuse_horizontal_illuminance(self):
        """
        :return: diffuse horizontal illuminance
        """
        return None if 'diffuse_horizontal_illuminance' not in self.mapping.keys() else QSeries(index=self.timestamps, data=self.data[self.mapping['diffuse_horizontal_illuminance'][0]].values * self.mapping['diffuse_horizontal_illuminance'][1])

    def get_zenith_illuminance(self):
        """
        :return: zenith illuminance
        """
        return None if 'zenith_illuminance' not in self.mapping.keys() else QSeries(index=self.timestamps, data=self.data[self.mapping['zenith_illuminance'][0]].values * self.mapping['zenith_illuminance'][1])

    def get_wind_direction(self):
        """
        :return: wind direction
        """
        return None if 'wind_direction' not in self.mapping.keys() else QSeries(index=self.timestamps, data=self.data[self.mapping['wind_direction'][0]].values * self.mapping['wind_direction'][1])

    def get_wind_speed(self):
        """
        :return: wind direction
        """
        return None if 'wind_speed' not in self.mapping.keys() else QSeries(index=self.timestamps, data=self.data[self.mapping['wind_speed'][0]].values * self.mapping['wind_speed'][1])

    def get_total_sky_cover(self):
        """
        :return: total sky cover
        """
        return None if 'total_sky_cover' not in self.mapping.keys() else QSeries(index=self.timestamps, data=self.data[self.mapping['total_sky_cover'][0]].values * self.mapping['total_sky_cover'][1])

    def get_opaque_sky_cover(self):
        """
        :return: opaque sky cover
        """
        return None if 'opaque_sky_cover' not in self.mapping.keys() else QSeries(index=self.timestamps, data=self.data[self.mapping['opaque_sky_cover'][0]].values * self.mapping['opaque_sky_cover'][1])

    def get_visibility(self):
        """
        :return: visibility
        """
        return None if 'visibility' not in self.mapping.keys() else QSeries(index=self.timestamps, data=self.data[self.mapping['visibility'][0]].values * self.mapping['visibility'][1])

    def get_ceiling_height(self):
        """
        :return: ceiling height
        """
        return None if 'ceiling_height' not in self.mapping.keys() else QSeries(index=self.timestamps, data=self.data[self.mapping['ceiling_height'][0]].values * self.mapping['ceiling_height'][1])


    def get_precipitable_water(self):
        """
        :return: precipitable water
        """
        return None if 'precipitable_water' not in self.mapping.keys() else QSeries(index=self.timestamps, data=self.data[self.mapping['precipitable_water'][0]].values * self.mapping['precipitable_water'][1])

    def get_aerosol_optical_depth(self):
        """
        :return: aerosol optical depth
        """
        return None if 'aerosol_optical_depth' not in self.mapping.keys() else QSeries(index=self.timestamps, data=self.data[self.mapping['aerosol_optical_depth'][0]].values * self.mapping['aerosol_optical_depth'][1])

    def get_snow_depth(self):
        """
        :return: snow depth
        """
        return None if 'snow_depth' not in self.mapping.keys() else QSeries(index=self.timestamps, data=self.data[self.mapping['snow_depth'][0]].values * self.mapping['snow_depth'][1])

    def get_days_since_last_snowfall(self):
        """
        :return: days since last snowfall
        """
        return None if 'days_since_last_snowfall' not in self.mapping.keys() else QSeries(index=self.timestamps, data=self.data[self.mapping['days_since_last_snowfall'][0]].values * self.mapping['days_since_last_snowfall'][1])

    def get_albedo(self):
        """
        :return: albedo
        """
        return None if 'albedo' not in self.mapping.keys() else QSeries(index=self.timestamps, data=self.data[self.mapping['albedo'][0]].values * self.mapping['albedo'][1])

    def get_liquid_precipitation_depth(self):
        """
        :return: liquid precipitation depth
        """
        return None if 'liquid_precipitation_depth' not in self.mapping.keys() else QSeries(index=self.timestamps, data=self.data[self.mapping['liquid_precipitation_depth'][0]].values * self.mapping['liquid_precipitation_depth'][1])

    def get_liquid_precipitation_quantity(self):
        """
        :return: liquid precipitation quantity
        """
        return None if 'liquid_precipitation_quantity' not in self.mapping.keys() else QSeries(index=self.timestamps, data=self.data[self.mapping['liquid_precipitation_quantity'][0]].values * self.mapping['liquid_precipitation_quantity'][1])

    def get_zenith_angle_sun(self):
        """
        :return: zenith angle sun
        """
        return None if 'zenith_angle_sun' not in self.mapping.keys() else QSeries(index=self.timestamps, data=self.data[self.mapping['zenith_angle_sun'][0]].values * self.mapping['zenith_angle_sun'][1])

    def get_azimuth_angle_sun(self):
        """
        :return: azimuth angle sun
        """
        return None if 'azimuth_angle_sun' not in self.mapping.keys() else QSeries(index=self.timestamps, data=self.data[self.mapping['azimuth_angle_sun'][0]].values * self.mapping['azimuth_angle_sun'][1])

    def get_sky_temperature(self):
        """
        :return: mean radiant temperature
        """
        return None if 'sky_temperature' not in self.mapping.keys() else QSeries(index=self.timestamps, data=self.data[self.mapping['sky_temperature'][0]].values * self.mapping['sky_temperature'][1])

class BuildingLoader():
    """
    Class to load a building.

    Attributes:
        building_file: file in which details of the building are stored.
        x: position of the building on the x-axis
        y: position of the building on the y-axis
    """
    __metaclass__ = ABCMeta

    def __init__(self, building_file, x = 0.0, y = 0.0):
        """
        :param building_file: file in which details of the building are stored.
        :paran x: position of the building on the x-axis
        :paran y: position of the building on the y-axis
        """
        self.building_file = building_file
        self.x = x
        self.y = y

    def load(self):
        """
        Load the building
        :return: loaded building
        """
        building = Building(self.get_building_name())
        building.zones = self.get_building_zones()
        (x_center, y_center, z_center) = building.get_footprint().get_centroid()
        building.move(self.x - x_center, self.y - y_center)
        return building

    @abstractmethod
    def get_building_name(self):
        """
        :return: name of the building
        """
        pass

class IDFBuildingLoader(BuildingLoader):
    """
    Class to load a building from an IDF file

    Attributes:
        building_file: file in which details of the building are stored.
        idf_objects: IDF objects.
    """

    def __init__(self, building_file, x = 0.0, y = 0.0):
        """
        :param building_file: IDF file containing details of the building.
        :paran x: position of the building on the x-axis
        :paran y: position of the building on the y-axis
        """
        BuildingLoader.__init__(self, building_file, x, y)
        IDF.setiddname(os.path.join(os.environ.get('ENERGYPLUS'), 'Energy+.idd'))
        self.idf = IDF(building_file)

    def get_building_name(self):
        """
        :return: name of the building
        """
        return self.idf.idfobjects['BUILDING'][0].Name

    def get_building_zones(self):
        """
        :return: name of the building
        """
        zones = []
        for zone_info in self.idf.idfobjects['ZONE']:
            zone = Zone(zone_info.Name)
            for surface in self.idf.idfobjects['BUILDINGSURFACE:DETAILED']:
                if surface.Zone_Name == zone.name:
                    count = 0
                    for field_name in surface.obj:
                        if field_name == surface.Vertex_1_Xcoordinate:
                            break
                        else:
                            count += 1
                    number_points = int((len(surface.obj) - count) / 3)
                    points = np.zeros((number_points, 3))
                    offset = 0
                    for point_ID in range(number_points):
                        points[point_ID][0] = surface.obj[count + offset]
                        points[point_ID][1] = surface.obj[count + 1 + offset]
                        points[point_ID][2] = surface.obj[count + 2 + offset]
                        offset = offset + 3
                    if surface.Surface_Type == 'Wall':
                        exterior_wall = ExteriorWall(surface.Name, points)
                        for window_surface in self.idf.idfobjects['FENESTRATIONSURFACE:DETAILED']:
                            if window_surface.Building_Surface_Name == exterior_wall.name:
                                count_window = 0
                                for field_name in window_surface.obj:
                                    if field_name == window_surface.Vertex_1_Xcoordinate:
                                        break
                                    else:
                                        count_window += 1
                                window_points = np.zeros((4, 3))
                                window_offset = 0
                                for point_ID in range(4):
                                    window_points[point_ID][0] = window_surface.obj[count_window + window_offset]
                                    window_points[point_ID][1] = window_surface.obj[count_window + 1 + window_offset]
                                    window_points[point_ID][2] = window_surface.obj[count_window + 2 + window_offset]
                                    window_offset = window_offset + 3
                                exterior_wall.windows.append(Surface(window_surface.name, window_points))
                        zone.exterior_walls.append(exterior_wall)
                    elif surface.Surface_Type == 'Floor':
                        zone.ground_floor = Surface(surface.Name, points)
                    elif surface.Surface_Type == 'Roof':
                        zone.roofs.append(Surface(surface.Name, points))
            for people in self.idf.idfobjects['PEOPLE']:
                if people.Zone_or_ZoneList_or_Space_or_SpaceList_Name == zone.name:
                    week_schd, weekend_schd = self.__get_schedules(people.Number_of_People_Schedule_Name, self.idf)
                    num_people = float(people.Number_of_People)
                    fraction_radiant = 0.0 if people.Fraction_Radiant == '' else float(people.Fraction_Radiant)
                    fraction_sensible = 0.0 if people.Sensible_Heat_Fraction == '' else float(people.Sensible_Heat_Fraction)
                    metabolic_heat_rate = 0.0
                    for schd in self.idf.idfobjects['SCHEDULE:COMPACT']:
                        if people.Activity_Level_Schedule_Name == schd.Name:
                            metabolic_heat_rate = float(schd.obj[6])
                    zone.sensible_internal_heat_sources.append(InternalHeat(fraction_sensible * metabolic_heat_rate * num_people, week_schedule=week_schd, weekend_schedule=weekend_schd))
                    zone.latent_internal_heat_sources.append(InternalHeat((1 - fraction_radiant) * (1 - fraction_sensible) * metabolic_heat_rate * num_people, week_schedule=week_schd, weekend_schedule=weekend_schd))
            for lights in self.idf.idfobjects['LIGHTS']:
                if lights.Zone_or_ZoneList_or_Space_or_SpaceList_Name == zone.name:
                    week_schd, weekend_schd = self.__get_schedules(lights.Schedule_Name, self.idf)
                    lighting_level = float(lights.Lighting_Level)
                    return_air_fraction = 0.0 if lights.Return_Air_Fraction == '' else float(lights.Return_Air_Fraction)
                    fraction_radiant = 0.0 if lights.Fraction_Radiant == '' else float(lights.Fraction_Radiant)
                    fraction_visible = 0.0 if lights.Fraction_Visible == '' else float(lights.Fraction_Visible)
                    fraction_replaceable = 0.0 if lights.Fraction_Replaceable == '' else float(lights.Fraction_Replaceable)
                    zone.sensible_internal_heat_sources.append(InternalHeat((1 - return_air_fraction) * (1 - fraction_radiant) * (1 - fraction_visible) * (1 - fraction_replaceable) * lighting_level, week_schedule=week_schd, weekend_schedule=weekend_schd))
            for electric_equipment in self.idf.idfobjects['ELECTRICEQUIPMENT']:
                if electric_equipment.Zone_or_ZoneList_or_Space_or_SpaceList_Name == zone.name:
                    week_schd, weekend_schd = self.__get_schedules(electric_equipment.Schedule_Name, self.idf)
                    design_level = float(electric_equipment.Design_Level)
                    fraction_latent = 0.0 if electric_equipment.Fraction_Latent == '' else float(electric_equipment.Fraction_Latent)
                    fraction_radiant = 0.0 if electric_equipment.Fraction_Radiant == '' else float(electric_equipment.Fraction_Radiant)
                    fraction_lost = 0.0 if electric_equipment.Fraction_Lost == '' else float(electric_equipment.Fraction_Lost)
                    zone.sensible_internal_heat_sources.append(InternalHeat((1 - fraction_latent) * (1 - fraction_radiant) * (1 - fraction_lost) * design_level, week_schedule=week_schd, weekend_schedule=weekend_schd))
                    zone.latent_internal_heat_sources.append(InternalHeat(fraction_latent * design_level, week_schedule=week_schd, weekend_schedule=weekend_schd))
            for ideal_load_system in self.idf.idfobjects['HVACTEMPLATE:ZONE:IDEALLOADSAIRSYSTEM']:
                if ideal_load_system.Zone_Name == zone.name:
                    zone.indoor_dehumidification_setpoint = ureg.Quantity(float(ideal_load_system.Dehumidification_Setpoint), ureg.percent)
                    for thermostat in self.idf.idfobjects['HVACTEMPLATE:THERMOSTAT']:
                        if ideal_load_system.Template_Thermostat_Name == thermostat.Name:
                            zone.indoor_temperature_setpoint = ureg.Quantity(float(thermostat.Constant_Cooling_Setpoint), ureg.degC)
            zones.append(zone)
        return zones

    def __get_schedules(self, name, idf):
        """
        :param name: name of schedule
        :param idf: IDF object containing all schedules
        :return: schedules for weeks and weekends
        """
        week_schd = np.zeros(24)
        is_week_schd_reading = False
        from_week_schd = 0
        to_week_schd = 0
        weekend_schd = np.zeros(24)
        is_weekend_schd_reading = False
        from_weekend_schd = 0
        to_weekend_schd = 0
        for schd in self.idf.idfobjects['SCHEDULE:COMPACT']:
            for n in range(len(schd.obj)):
                if is_week_schd_reading:
                    if 'Until:' in schd.obj[n]:
                        match = re.search(r"\d{2}:\d{2}", schd.obj[n])
                        hour, minute = map(int, match.group().split(":"))
                        to_week_schd = hour - 1
                    else:
                        week_schd[from_week_schd:to_week_schd] = float(schd.obj[n])
                        from_week_schd = to_week_schd
                    if from_week_schd == 23:
                        is_week_schd_reading = False
                elif is_weekend_schd_reading:
                    if 'Until:' in schd.obj[n]:
                        match = re.search(r"\d{2}:\d{2}", schd.obj[n])
                        hour, minute = map(int, match.group().split(":"))
                        to_weekend_schd = hour - 1
                    else:
                        weekend_schd[from_weekend_schd:to_weekend_schd] = float(schd.obj[n])
                        from_weekend_schd = to_weekend_schd
                    if from_weekend_schd == 23:
                        is_weekend_schd_reading = False
                elif schd.obj[n] == 'For: Weekdays':
                    is_week_schd_reading = True
                elif schd.obj[n] == 'For: Weekends':
                    is_weekend_schd_reading = True
        return week_schd, weekend_schd


class BuildingEnergyModel():
    """
    Class representing a building energy model.

    Attributes:
        building: building being modelled
        building_loader: loader of building
        outputs: outputs resulting from simulations using the building energy model
    """
    __metaclass__ = ABCMeta

    def __init__(self, building_loader):
        """
        :param building_loader: loader of building
        """
        self.building_loader = building_loader
        self.building = None
        self.outputs = None

    def get_start_date(self):
        """
        :return: start date to perform simulations using the building energy model
        """
        ext = os.path.splitext(self.building_loader.building_file)[1]
        if ext == '.idf':
            IDF.setiddname(os.path.join(os.environ.get('ENERGYPLUS'), 'Energy+.idd'))
            idf = IDF(self.building_loader.building_file)
            YEAR = int(idf.idfobjects['RUNPERIOD'][0].Begin_Year)
            MONTH = int(idf.idfobjects['RUNPERIOD'][0].Begin_Month)
            DAY = int(idf.idfobjects['RUNPERIOD'][0].Begin_Day_of_Month)
        return datetime(YEAR, MONTH, DAY,1, 0, 0)

    def get_end_date(self):
        """
        :return: end date to perform simulations using the building energy model
        """
        ext = os.path.splitext(self.building_loader.building_file)[1]
        if ext == '.idf':
            IDF.setiddname(os.path.join(os.environ.get('ENERGYPLUS'), 'Energy+.idd'))
            idf = IDF(self.building_loader.building_file)
            YEAR = int(idf.idfobjects['RUNPERIOD'][0].End_Year)
            MONTH = int(idf.idfobjects['RUNPERIOD'][0].End_Month)
            DAY = int(idf.idfobjects['RUNPERIOD'][0].End_Day_of_Month)
        return datetime(YEAR, MONTH, DAY, 0, 0, 0) + timedelta(days=1)

    def get_dt(self):
        """
        :return: timestep to perform simulations using the building energy model
        """
        ext = os.path.splitext(self.building_loader.building_file)[1]
        if ext == '.idf':
            IDF.setiddname(os.path.join(os.environ.get('ENERGYPLUS'), 'Energy+.idd'))
            idf = IDF(self.building_loader.building_file)
            DT = 3600 / int(idf.idfobjects['TIMESTEP'][0].Number_of_Timesteps_per_Hour)
        return timedelta(seconds=DT)

    @abstractmethod
    def update(self):
        """
        Update the modelled building with respect to outputs of simulations.
        """
        pass

class EnergyPlusModel(BuildingEnergyModel):
    """
    Class representing an EnergyPlus model

    Attributes:
        building: building being modelled
        building_loader: loader of building
        outputs: outputs resulting from simulations using the building energy model
    """

    def __init__(self, building_loader):
        """
        :param building_loader: loader of building
        """
        BuildingEnergyModel.__init__(self, building_loader)


    def update(self):
        """
        Update the modelled building with respect to outputs of simulations.
        """
        idcols = self.outputs.keys().to_list()
        for zone in self.building.zones:
            zone_name = zone.name.upper()
            idx_cooling_load = np.where([(zone_name in s) for s in idcols])[0]
            if 'Zone Ideal Loads Zone Sensible Cooling Rate' in idcols[idx_cooling_load[0]]:
                zone.sensible_load = pd.Series(self.outputs[idcols[idx_cooling_load[0]]] * ureg.watt, index = self.outputs.index)
                zone.latent_load = pd.Series(self.outputs[idcols[idx_cooling_load[1]]] * ureg.watt, index = self.outputs.index)
            else:
                zone.sensible_load = pd.Series(self.outputs[idcols[idx_cooling_load[1]]] * ureg.watt, index=self.outputs.index)
                zone.latent_load = pd.Series(self.outputs[idcols[idx_cooling_load[0]]] * ureg.watt, index=self.outputs.index)
            for roof in zone.roofs:
                roof_name = roof.name.upper()
                idx_roof_surface_temperature = np.where([(roof_name in s) for s in idcols])[0]
                roof.temperature = pd.Series(self.outputs[idcols[idx_roof_surface_temperature[0]]] * ureg.degC, index = self.outputs.index)
            for exterior_wall in zone.exterior_walls:
                exterior_wall_name = exterior_wall.name.upper()
                idx_exterior_wall_surface_temperature = np.where([(exterior_wall_name in s) for s in idcols])[0]
                exterior_wall.temperature = pd.Series(self.outputs[idcols[idx_exterior_wall_surface_temperature[0]]] * ureg.degC, index = self.outputs.index)
                for window in exterior_wall.windows:
                    window_name = window.name.upper()
                    idx_window_surface_temperature = np.where([(window_name in s) for s in idcols])[0]
                    window.temperature = pd.Series(self.outputs[idcols[idx_window_surface_temperature[0]]])
            ground_floor_name = zone.ground_floor.name.upper()
            idx_ground_floor_surface_temperature = np.where([(ground_floor_name in s) for s in idcols])[0]
            zone.ground_floor.temperature = pd.Series(self.outputs[idcols[idx_ground_floor_surface_temperature[0]]] * ureg.degC, index=self.outputs.index)

class DataDrivenBuildingEnergyModel(BuildingEnergyModel):
    """
    Class representing a data driven building energy model.

    Attributes:
        building: building being modelled.
        building_loader: loader of building.
        outputs: outputs resulting from simulations using the building energy model.
        weather_data: weather data to be considered for boundary conditions of the data driven building energy model.
        training_split_ratio: ratio between the size of the training set and the total data set over the period of simulation.
        target: building energy data used for optimization of the data driven model.
        start_date: starting date of simulation.
        end_date: ending date of simulation.
        dt: timestep of simulation.
        output_dir: directory where outputs are saved.
    """
    __metaclass__ = ABCMeta

    def __init__(self, building_loader, weather_data = None, training_split_ratio = 0.0, output_dir = '.'):
        """
        :param building_loader: loader of building
        """
        BuildingEnergyModel.__init__(self, building_loader)
        self.weather_data = weather_data
        self.training_split_ratio = training_split_ratio
        self.output_dir = output_dir
        self.target = None

    def update(self):
        """
        Update the modelled building with respect to outputs of simulations.
        """
        file_path = os.path.join(self.output_dir, self.building.name + '.csv')
        if os.path.exists(file_path):
            os.remove(file_path)
        self.outputs.to_csv(file_path, index_label='Date/Time')

    def get_target_building_load(self):
        """
        :return: the target building load
        """
        return self.building.get_building_load_measurements()

    @abstractmethod
    def train(self, start_date, end_date, dt):
        """
        Train the data driven building energy model
        :param start_date: date to start simulation
        :param end_date: date to end simulation
        :param dt: timestamp of simulation
        """
        pass

    @abstractmethod
    def test(self, start_date, end_date, dt):
        """
        Test the data driven building energy model
        :param start_date: date to start simulation
        :param end_date: date to end simulation
        :param dt: timestamp of simulation
        """
        pass

    @abstractmethod
    def get_previous_error_building_load(self, start_date, end_date, dt):
        """
        Previous error made on building load
        :param start_date: date to start simulation
        :param end_date: date to end simulation
        :param dt: timestamp of simulation
        """
        pass

    @abstractmethod
    def get_current_error_building_load(self, start_date, end_date, dt):
        """
        Current error made on building load
        :param start_date: date to start simulation
        :param end_date: date to end simulation
        :param dt: timestamp of simulation
        """
        pass

    @abstractmethod
    def update_previous_solution(self):
        """
        Update previous solution found by the data driven building energy model
        """
        pass

class LinearStateSpaceBuildingEnergyModel(DataDrivenBuildingEnergyModel):
    """
    Class representing a single zone model

    Attributes:
        building: building being modelled
        building_loader: loader of building
        outputs: outputs resulting from simulations using the building energy model
        training_split_ratio: ratio between the size of the training set and the total data set over the period of simulation.
        start_date: starting date of simulation.
        end_date: ending date of simulation.
        dt: timestep of simulation.
        previous_lumped_thermal_parameters: previously found lumped thermal parameters.
        current_lumped_thermal_parameters: currently found lumped thermal parameters.
        error_function: error function to optimize the building load.
    """

    def __init__(self, building_loader, weather_data = None, training_split_ratio = 0.0, output_dir = '.', error_function = RootMeanSquareError()):
        """
        :param building_loader: loader of building
        """
        DataDrivenBuildingEnergyModel.__init__(self, building_loader, weather_data, training_split_ratio, output_dir)
        self.previous_lumped_thermal_parameters = []
        self.current_lumped_thermal_parameters = []
        self.error_function = error_function
        self.current_start_date = None
        self.current_end_date = None
        self.current_dt = None
        self.U = None

    def get_input_vectors(self, start_date, end_date, dt):
        """
        :param start_date: start date of simulations
        :param end_date: end date of simulations
        :param dt: timestep of simulations
        """
        input_vectors = []
        input_vectors.append(pd.Series(data=self.building.get_indoor_temperature_setpoints().m, index=pd.date_range(start=start_date, end=end_date, freq=dt)).values.tolist())
        input_vectors.append(self.weather_data['dry_bulb_temperature'].resample(dt).interpolate()[start_date:end_date + dt].values.tolist())
        input_vectors.append(self.weather_data['sky_temperature'].resample(dt).interpolate()[start_date:end_date + dt].values.tolist())
        input_vectors.append(self.building.get_sensible_internal_heat_gains(start=start_date, end=end_date, dt=dt).values.tolist())
        input_vectors.append(pd.Series(data=self.building.get_indoor_specific_humidity_setpoints().to(ureg.gram/ureg.kilogram).m, index=pd.date_range(start=start_date, end=end_date, freq=dt)).values.tolist())
        input_vectors.append(self.weather_data['specific_humidity'].resample(dt).interpolate()[start_date:end_date + dt].values.tolist())
        input_vectors.append(self.building.get_latent_internal_heat_gains(start=start_date, end=end_date, dt=dt).values.tolist())
        input_vectors.append(self.weather_data['direct_normal_radiation'].resample(dt).interpolate()[start_date:end_date + dt].values.tolist())
        input_vectors.append(self.weather_data['diffuse_horizontal_radiation'].resample(dt).interpolate()[start_date:end_date + dt].values.tolist())
        return np.asarray(input_vectors)

    def get_state_matrix(self, lumped_thermal_parameters):
        """
        :return: state matrix
        """
        thermal_capacitance_building_exterior_surface = lumped_thermal_parameters[0]
        thermal_capacitance_building_interior_surface = lumped_thermal_parameters[1]
        thermal_capacitance_building_internal_mass = lumped_thermal_parameters[2]
        thermal_resistance_outdoor_air_exterior_surface = lumped_thermal_parameters[3]
        thermal_resistance_sky_exterior_surface = lumped_thermal_parameters[4]
        thermal_resistance_interior_surface_exterior_surface = lumped_thermal_parameters[5]
        thermal_resistance_interior_surface_indoor_air = lumped_thermal_parameters[6]
        thermal_resistance_interior_surface_internal_mass = lumped_thermal_parameters[7]
        thermal_resistance_indoor_air_internal_mass = lumped_thermal_parameters[8]
        A = np.zeros((3, 3))
        A[0, 0] = -(1.0 / thermal_resistance_outdoor_air_exterior_surface +
                    1.0 / thermal_resistance_sky_exterior_surface +
                    1.0 / thermal_resistance_interior_surface_exterior_surface) / thermal_capacitance_building_exterior_surface
        A[0, 1] = 1.0 / (thermal_resistance_interior_surface_exterior_surface * thermal_capacitance_building_exterior_surface)
        A[1, 0] = 1.0 / (thermal_resistance_interior_surface_exterior_surface * thermal_capacitance_building_interior_surface)
        A[1, 1] = - (1.0 / thermal_resistance_interior_surface_exterior_surface +
                     1.0 / thermal_resistance_interior_surface_indoor_air +
                     1.0 / thermal_resistance_interior_surface_internal_mass) / thermal_capacitance_building_interior_surface
        A[1, 2] = 1.0 / (thermal_resistance_interior_surface_internal_mass * thermal_capacitance_building_interior_surface)
        A[2, 1] = 1.0 / (thermal_resistance_interior_surface_internal_mass * thermal_capacitance_building_internal_mass)
        A[2, 2] = - (1.0 / thermal_resistance_interior_surface_internal_mass +
                     1.0 / thermal_resistance_indoor_air_internal_mass) / thermal_capacitance_building_internal_mass
        return A

    def get_input_matrix(self, lumped_thermal_parameters):
        """
        :return: input matrix
        """
        thermal_capacitance_building_exterior_surface = lumped_thermal_parameters[0]
        thermal_capacitance_building_interior_surface = lumped_thermal_parameters[1]
        thermal_capacitance_building_internal_mass = lumped_thermal_parameters[2]
        thermal_resistance_outdoor_air_exterior_surface = lumped_thermal_parameters[3]
        thermal_resistance_sky_exterior_surface = lumped_thermal_parameters[4]
        thermal_resistance_interior_surface_indoor_air = lumped_thermal_parameters[6]
        thermal_resistance_indoor_air_internal_mass = lumped_thermal_parameters[8]
        fraction_direct_normal_radiation = lumped_thermal_parameters[9]
        fraction_diffuse_horizontal_radiation = lumped_thermal_parameters[10]

        B = np.zeros((3, 9))
        B[0, 1] = 1.0 / (thermal_resistance_outdoor_air_exterior_surface * thermal_capacitance_building_exterior_surface)
        B[0, 2] = 1.0 / (thermal_resistance_sky_exterior_surface * thermal_capacitance_building_exterior_surface)
        B[0, 7] = fraction_direct_normal_radiation / thermal_capacitance_building_exterior_surface
        B[0, 8] = fraction_diffuse_horizontal_radiation / thermal_capacitance_building_exterior_surface
        B[1, 0] = 1.0 / (thermal_resistance_interior_surface_indoor_air * thermal_capacitance_building_interior_surface)
        B[2, 0] = 1.0 / (thermal_resistance_indoor_air_internal_mass * thermal_capacitance_building_internal_mass)
        return B

    def get_output_matrix(self, lumped_thermal_parameters):
        """
        :return: output matrix
        """
        thermal_resistance_interior_surface_indoor_air = lumped_thermal_parameters[6]
        thermal_resistance_indoor_air_internal_mass = lumped_thermal_parameters[8]

        C = np.zeros((2, 3))
        C[0, 1] = 1.0 / thermal_resistance_interior_surface_indoor_air
        C[0, 2] = 1.0 / thermal_resistance_indoor_air_internal_mass
        return C

    def get_direct_transition_matrix(self, lumped_thermal_parameters):
        """
        :return: direct transition matrix
        """
        thermal_resistance_interior_surface_indoor_air = lumped_thermal_parameters[6]
        thermal_resistance_indoor_air_internal_mass = lumped_thermal_parameters[8]
        thermal_resistance_outdoor_air_indoor_air = lumped_thermal_parameters[11]
        mass_resistance_outdoor_air_indoor_air = lumped_thermal_parameters[12]

        D = np.zeros((2, 9))
        D[0, 0] = - (1.0 / thermal_resistance_interior_surface_indoor_air +
                     1.0 / thermal_resistance_indoor_air_internal_mass +
                     1.0 / thermal_resistance_outdoor_air_indoor_air)
        D[0, 1] = 1.0 / thermal_resistance_outdoor_air_indoor_air
        D[0, 3] = 1.0
        D[1, 4] = - 1.0 / mass_resistance_outdoor_air_indoor_air
        D[1, 5] = 1.0 / mass_resistance_outdoor_air_indoor_air
        D[1, 6] = 1.0
        return D

    def get_state_outputs(self, lumped_thermal_parameters, start_date, end_date, dt):
        must_update_U = (self.current_start_date is None) | \
                        (self.current_end_date is None) | \
                        (self.current_dt is None) | \
                        (self.current_start_date != start_date) | \
                        (self.current_end_date != end_date) | \
                        (self.current_dt != dt)
        if must_update_U:
            self.U = np.transpose(self.get_input_vectors(start_date, end_date, dt))
            self.current_start_date = start_date
            self.current_end_date = end_date
            self.current_dt = dt
        A = self.get_state_matrix(lumped_thermal_parameters)
        B = self.get_input_matrix(lumped_thermal_parameters)
        C = self.get_output_matrix(lumped_thermal_parameters)
        D = self.get_direct_transition_matrix(lumped_thermal_parameters)
        sys = sig.StateSpace(A, B, C, D)
        sys_d = sys.to_discrete(dt=dt.seconds, method='backward_diff')
        x0 = np.asarray([35.0, 30.0, 20.0])
        t, Y, X = sig.dlsim(sys_d, u=self.U, x0=x0)
        X = np.transpose(X)
        Y = np.transpose(Y)
        return (Y, X)

    def train(self, start_date, end_date, dt):
        """
        Train the data driven building energy model
        :param start_date: date to start simulation
        :param end_date: date to end simulation
        :param dt: timestamp of simulation
        """
        lb = np.asarray([1e4, 1e4, 1e4, 1e-4, 1e-3, 1e-3, 1e-1, 1e-3, 1e-1, 0.05, 0.05, 1e-7, 1e-8])
        ub = np.asarray([1e6, 1e6, 1e6, 1e-1, 1e0, 1e0, 1e1, 1e0, 1e1, 1.0, 1.0, 1e-2, 1e-2])
        N = len(lb)
        if len(self.previous_lumped_thermal_parameters) == 0:
            self.previous_lumped_thermal_parameters = np.random.uniform(lb, ub, size = N)
        problem = self.MultiObjectiveProblem(n_var=N, n_obj=3, lb=lb, ub=ub, bem=self.copy(),
                                             start_date=start_date, end_date=end_date, dt=dt)
        algorithm = NSGA2(pop_size=100, n_offsprings=25, sampling=FloatRandomSampling(),
                          crossover=SBX(prob=0.9, eta=15), mutation=PM(eta=20),
                          eliminate_duplicates=True)
        termination = get_termination("n_gen", 100)
        results = minimize(problem, algorithm, termination, seed=1, save_history=True, verbose=True)
        self.current_lumped_thermal_parameters = results.X[np.argmin(results.F[:, 0]), :]
        if self.get_previous_error_building_load(start_date, end_date, dt) < self.get_current_error_building_load(start_date, end_date, dt):
            Y, X = self.get_state_outputs(self.previous_lumped_thermal_parameters, start_date, end_date, dt)
        else:
            Y, X = self.get_state_outputs(self.current_lumped_thermal_parameters, start_date, end_date, dt)
        num_zones = len(self.building.zones)
        for zone in self.building.zones:
            zone.sensible_load = pd.Series(index=pd.date_range(start=start_date, end=end_date, freq=dt), data=Y[0, :]) / num_zones
            zone.latent_load = pd.Series(index=pd.date_range(start=start_date, end=end_date, freq=dt), data=Y[1, :]) / num_zones
            for exterior_wall in zone.exterior_walls:
                exterior_wall.temperature = pd.Series(index=pd.date_range(start=start_date, end=end_date, freq=dt), data=X[0, :])
                for window in exterior_wall.windows:
                    window.temperature = pd.Series(index=pd.date_range(start=start_date, end=end_date, freq=dt), data=X[0, :])
        self.__save_and_print_solution()

    def test(self, start_date, end_date, dt):
        """
        Test the data driven building energy model
        :param start_date: date to start simulation
        :param end_date: date to end simulation
        :param dt: timestamp of simulation
        """
        Y, X = self.get_state_outputs(self.current_lumped_thermal_parameters, start_date, end_date, dt)
        num_zones = len(self.building.zones)
        for zone in self.building.zones:
            if zone.sensible_load is not None:
                zone.sensible_load = pd.concat([zone.sensible_load, pd.Series(index=pd.date_range(start=start_date, end=end_date, freq=dt), data=Y[0, :]) / num_zones])
            else:
                zone.sensible_load = pd.Series(index=pd.date_range(start=start_date, end=end_date, freq=dt), data=Y[0, :]) / num_zones
            if zone.latent_load is not None:
                zone.latent_load = pd.concat([zone.latent_load, pd.Series(index=pd.date_range(start=start_date, end=end_date, freq=dt), data=Y[1, :]) / num_zones])
            else:
                zone.latent_load = pd.Series(index=pd.date_range(start=start_date, end=end_date, freq=dt), data=Y[1, :]) / num_zones
            for exterior_wall in zone.exterior_walls:
                if exterior_wall.temperature is not None:
                    exterior_wall.temperature = pd.concat([exterior_wall.temperature, pd.Series(index=pd.date_range(start=start_date, end=end_date, freq=dt), data=X[0, :])])
                else:
                    exterior_wall.temperature = pd.Series(index=pd.date_range(start=start_date, end=end_date, freq=dt), data=X[0, :])
                for window in exterior_wall.windows:
                    if window.temperature is not None:
                        window.temperature = pd.concat([window.temperature, pd.Series(index=pd.date_range(start=start_date, end=end_date, freq=dt), data=X[0, :])])
                    else:
                        window.temperature = pd.Series(index=pd.date_range(start=start_date, end=end_date, freq=dt), data=X[0, :])

    def get_previous_error_building_load(self, start_date, end_date, dt):
        """
        Previous error made on building load
        :param start_date: date to start simulation
        :param end_date: date to end simulation
        :param dt: timestamp of simulation
        """
        Y, X = self.get_state_outputs(self.previous_lumped_thermal_parameters, start_date, end_date, dt)
        return self.error_function.err(Y[0, :] + Y[1, :],
                                       self.target['total_sensible_load'].resample(dt).interpolate()[start_date:end_date + dt].values +
                                       self.target['total_latent_load'].resample(dt).interpolate()[start_date:end_date + dt].values)

    def get_current_error_building_load(self, start_date, end_date, dt):
        """
        Current error made on building load
        :param start_date: date to start simulation
        :param end_date: date to end simulation
        :param dt: timestamp of simulation
        """
        Y, X = self.get_state_outputs(self.current_lumped_thermal_parameters, start_date, end_date, dt)
        return self.error_function.err(Y[0, :] + Y[1, :],
                                       self.target['total_sensible_load'].resample(dt).interpolate()[start_date:end_date + dt].values +
                                       self.target['total_latent_load'].resample(dt).interpolate()[start_date:end_date + dt].values)

    def update_previous_solution(self):
        """
        Update previous solution found by the data driven building energy model
        """
        self.current_lumped_thermal_parameters = self.previous_lumped_thermal_parameters

    def copy(self):
        """
        Copy of the linear state space urban microclimate model
        :return: copy of the linear state space urban microclimate model
        """
        instance = LinearStateSpaceBuildingEnergyModel(self.building_loader, weather_data=self.weather_data)
        instance.building_loader = None
        instance.building = self.building
        instance.target = self.target
        return instance

    def __save_and_print_solution(self):
        results = {}
        results['exterior_wall_thermal_capacitance'] = self.current_lumped_thermal_parameters[0]
        results['interior_wall_thermal_capacitance'] = self.current_lumped_thermal_parameters[1]
        results['internal_mass_thermal_capacitance'] = self.current_lumped_thermal_parameters[2]
        results['outdoor_air_exterior_wall_thermal_resistance'] = self.current_lumped_thermal_parameters[3]
        results['sky_exterior_wall_thermal_resistance'] = self.current_lumped_thermal_parameters[4]
        results['wall_interior_exterior_wall_thermal_resistance'] = self.current_lumped_thermal_parameters[5]
        results['indoor_air_interior_wall_thermal_resistance'] = self.current_lumped_thermal_parameters[6]
        results['internal_mass_interior_wall_thermal_resistance'] = self.current_lumped_thermal_parameters[7]
        results['indoor_air_internal_mass_thermal_resistance'] = self.current_lumped_thermal_parameters[8]
        results['fraction_direct_normal_radiation'] = self.current_lumped_thermal_parameters[9]
        results['fraction_diffuse_horizontal_radiation'] = self.current_lumped_thermal_parameters[10]
        results['indoor_air_outdoor_air_thermal_resistance'] = self.current_lumped_thermal_parameters[11]
        results['indoor_air_outdoor_air_mass_resistance'] = self.current_lumped_thermal_parameters[12]
        with open(os.path.join(self.output_dir, self.building.name + '_trained_parameters.json'), 'w') as f:
            json.dump(results, f)
        print('================================================')
        print('Current trained solution')
        print('================================================')
        print(f'Exterior wall thermal capacitance (J/K) = {self.current_lumped_thermal_parameters[0]}')
        print(f'Interior wall thermal capacitance (J/K) = {self.current_lumped_thermal_parameters[1]}')
        print(f'Internal mass thermal capacitance (J/K) = {self.current_lumped_thermal_parameters[2]}')
        print(f'Thermal resistance outdoor air-wall exterior surface (K/W) = {self.current_lumped_thermal_parameters[3]}')
        print(f'Thermal resistance sky temperature-wall exterior surface (K/W) = {self.current_lumped_thermal_parameters[4]}')
        print(f'Thermal resistance wall interior surface-wall exterior surface (K/W) = {self.current_lumped_thermal_parameters[5]}')
        print(f'Thermal resistance indoor air-wall interior surface (K/W) = {self.current_lumped_thermal_parameters[6]}')
        print(f'Thermal resistance internal mass-wall interior surface (K/W) = {self.current_lumped_thermal_parameters[7]}')
        print(f'Thermal resistance indoor air-internal mass (K/W) = {self.current_lumped_thermal_parameters[8]}')
        print(f'Fraction direct normal radiation (0-1) = {self.current_lumped_thermal_parameters[9]}')
        print(f'Fraction diffuse horizontal radiation (0-1) = {self.current_lumped_thermal_parameters[10]}')
        print(f'Thermal resistance indoor air-outdoor air (K/W) = {self.current_lumped_thermal_parameters[11]}')
        print(f'Mass resistance indoor air-outdoor air (g/kg-W) = {self.current_lumped_thermal_parameters[12]}')

    class MultiObjectiveProblem(ElementwiseProblem):
        """
        Class stating the multi objective problem we would like to optimise to find convective heat transfer coefficients.

        Attributes:
            umm: the linear state space urban microclimate model to optimize
            start_date: date to start simulation
            end_date: date to end simulation
            dt: timestamp of simulation
        """

        def __init__(self, n_var, n_obj, lb, ub, bem, start_date, end_date, dt):
            """
            :param n_var: number of variables to optimize
            :param n_obj: number of objectives to optimize
            :param lb: lower bounds of each variable
            :param ub: upper bounds of each variable
            :param bem: building energy model to optimize
            :param start_date: date to start simulation
            :param end_date: date to end simulation
            :param dt: timestamp of simulation
            """
            ElementwiseProblem.__init__(self, n_var=n_var, n_obj=n_obj, xl=lb, xu=ub)
            self.bem = bem
            self.start_date = start_date
            self.end_date = end_date
            self.dt = dt
            self.target_total_sensible_load = bem.target['total_sensible_load'].resample(dt).interpolate()[start_date:end_date + dt].values
            self.target_total_latent_load = bem.target['total_latent_load'].resample(dt).interpolate()[start_date:end_date + dt].values
            self.target_average_wall_surface_temperature = bem.target['average_wall_surface_temperature'].resample(dt).interpolate()[start_date:end_date + dt].values

        def _evaluate(self, x, out, *args, **kwargs):
            """
            :param x: list of heat transfer coefficients to optimize
            :param out: objectives to optimize
            """
            Y, X = self.bem.get_state_outputs(x, self.start_date, self.end_date, self.dt)
            error_function = RootMeanSquareError()
            out["F"] = [error_function.err(Y[0, :], self.target_total_sensible_load),
                        error_function.err(Y[1, :], self.target_total_latent_load),
                        error_function.err(X[0, :], self.target_average_wall_surface_temperature)]

class BuildingEnergySimulationPool():
    """
    Pool to perform simulations of a sequence of building energy models in parallel.

    Attributes:
        weather_data: weather data to perform simulations of building energy models.
        weather_data_loader: loader of weather data.
        nproc: number of processors to run in parallel.
        pool: list of building energy models used for parallel simulations.
    """
    __metaclass__ = ABCMeta

    def __init__(self, weather_file, nproc = 2):
        """
        :param weather_data_loader: loader of weather data.
        :param nproc: number of processors to run in parallel.
        """
        self.weather_file = weather_file
        self.nproc = nproc
        self.pool = []

    def run(self):
        """
        Perform building energy simulations in parallel.
        :return: list of buildings resulting from simulation
        """
        self.create_simulation_environment()
        for bem in self.pool:
            if bem.building is None:
                bem.building = bem.building_loader.load()
        self.run_parallel_simulation()
        for bem in self.pool:
            while True:
                try:
                    bem.outputs = self.get_building_outputs(bem.building.name)
                    if not bem.outputs is None:
                        bem.update()
                    break
                except FileNotFoundError:
                    pass
                except PermissionError:
                    pass
        self.cleanup()

    @abstractmethod
    def create_simulation_environment(self):
        """
        Create simulation environment to perform simulations using the pool of building energy models
        """
        pass

    @abstractmethod
    def run_parallel_simulation(self):
        """
        Run parallel building energy simulations.
        """
        pass

    @abstractmethod
    def get_building_outputs(self, building_name):
        """
        :param building_name: name of the building
        :return: outputs of the simulation for the building
        """
        pass

    @abstractmethod
    def cleanup(self):
        """
        Cleanup the simulation environment.
        """
        pass

class EnergyPlusSimulationPool(BuildingEnergySimulationPool):
    """
    Pool to perform simulations using EnergyPlus in parallel.

    Attributes:
        nproc: number of processors to run in parallel.
        pool: list of building energy models used for parallel simulations.
        output_dir: directory in which parallel simulations must be performed and outputs being stored.
    """
    def __init__(self, weather_file, nproc = 2, output_dir = '.', year = date.today().year):
        BuildingEnergySimulationPool.__init__(self, weather_file, nproc)
        self.output_dir = output_dir
        self.year = year

    def create_simulation_environment(self):
        """
        Create simulation environment to perform simulations using the pool of building energy models
        """
        ENERGYPLUS_DIR = os.getenv('ENERGYPLUS')
        if (self.output_dir != '.') and (not os.path.isdir(self.output_dir)):
            os.mkdir(self.output_dir)
        for bem in self.pool:
            shutil.copy(bem.building_loader.building_file, self.output_dir)
        if platform.system() == 'Windows':
            shutil.copy(os.path.join(ENERGYPLUS_DIR, 'RunDirMulti.bat'), self.output_dir)
        for f in glob.glob(os.path.join(self.output_dir, '*.csv')):
            os.remove(f)

    def run_parallel_simulation(self):
        """
        Run parallel building energy simulations.
        """
        weather_file_name = os.path.splitext(os.path.basename(self.weather_file))[0]
        if platform.system() == 'Windows':
            p = Popen(f"RunDirMulti.bat {weather_file_name}  {str(self.nproc)}", cwd=self.output_dir, shell=True)
            p.communicate()
        elif platform.system() == 'Linux':
            if self.output_dir.endswith("/"):
                input_files = [self.output_dir + file for file in os.listdir(self.output_dir) if file.endswith(".idf")]
            else:
                input_files = [self.output_dir + "/" + file for file in os.listdir(self.output_dir) if file.endswith(".idf")]
            for input_file in input_files:
                command = [f"energyplus -x -r -w {self.weather_file} -p {os.path.basename(input_file)} -d {os.path.dirname(input_file)} -r {input_file}"]
                subprocess.run(command)

    def get_building_outputs(self, building_name):
        """
        :param building_name: name of the building
        :return: outputs of the simulation for the building
        """
        try:
            if platform.system() == 'Windows':
                output_file = os.path.join(self.output_dir, building_name + '.csv')
            elif platform.system() == 'Linux':
                output_file = os.path.join(self.output_dir, building_name + '.idfout.csv')
            df = pd.read_csv(output_file, index_col=[0])
            idxs = [str(self.year) + '/' + s for s in df.index.tolist()]
            idxd = []
            for sd in idxs:
                sd_no_whitespaces = sd.replace(' ', '')
                sd_modified = sd_no_whitespaces[:10] + " " + sd_no_whitespaces[10:]
                if '24:' in sd:
                    s = sd_modified.replace('24:', '00:')
                    d = datetime.strptime(s, '%Y/%m/%d %H:%M:%S')
                    idxd.append(d + timedelta(days=1))
                else:
                    idxd.append(datetime.strptime(sd_modified, '%Y/%m/%d %H:%M:%S'))
            return df.set_index(pd.DatetimeIndex(idxd))
        except pd.errors.EmptyDataError:
            return None

    def cleanup(self):
        """
        Cleanup the simulation environment.
        """
        for f in glob.glob(os.path.join(self.output_dir, '*.audit')):
            os.remove(f)
        for f in glob.glob(os.path.join(self.output_dir, '*.bnd')):
            os.remove(f)
        for f in glob.glob(os.path.join(self.output_dir, '*.eio')):
            os.remove(f)
        for f in glob.glob(os.path.join(self.output_dir, '*.err')):
            os.remove(f)
        for f in glob.glob(os.path.join(self.output_dir, '*.eso')):
            os.remove(f)
        for f in glob.glob(os.path.join(self.output_dir, '*.expidf')):
            os.remove(f)
        for f in glob.glob(os.path.join(self.output_dir, '*.idf')):
            os.remove(f)
        for f in glob.glob(os.path.join(self.output_dir, '*.mdd')):
            os.remove(f)
        for f in glob.glob(os.path.join(self.output_dir, '*.mtd')):
            os.remove(f)
        for f in glob.glob(os.path.join(self.output_dir, '*.mtr')):
            os.remove(f)
        for f in glob.glob(os.path.join(self.output_dir, '*.rdd')):
            os.remove(f)
        for f in glob.glob(os.path.join(self.output_dir, '*.rvaudit')):
            os.remove(f)
        for f in glob.glob(os.path.join(self.output_dir, '*.shd')):
            os.remove(f)
        for f in glob.glob(os.path.join(self.output_dir, '*.sql')):
            os.remove(f)
        for f in glob.glob(os.path.join(self.output_dir, '*.svg')):
            os.remove(f)
        for f in glob.glob(os.path.join(self.output_dir, '*.html')):
            os.remove(f)
        for f in glob.glob(os.path.join(self.output_dir, 'tempsim*')):
            shutil.rmtree(f)
        os.remove(os.path.join(self.output_dir, 'RunDirMulti.bat'))


class DataDrivenBuildingEnergySimulationPool(BuildingEnergySimulationPool):
    """
    Pool to perform simulations using EnergyPlus in parallel.

    Attributes:
        nproc: number of processors to run in parallel.
        pool: list of building energy models used for parallel simulations.
        start_date: start date of simulations
        end_date: end date of simulations
        dt: timestep of simulations
        building_energy_data_dir: directory in which building energy data to emulate are stored
        output_dir: directory in which simulation outputs will be stored
    """
    def __init__(self, weather_file, nproc = 2, building_energy_data_dir = '.', output_dir = '.',
                 year = date.today().year, mapping = {}, date_format = '%Y-%m-%d %H:%M:%S',
                 time_zone='GMT'):
        BuildingEnergySimulationPool.__init__(self, weather_file, nproc)
        self.building_energy_data_dir = building_energy_data_dir
        self.output_dir = output_dir
        self.year = year
        self.mapping = mapping
        self.date_format = date_format
        self.time_zone = time_zone

    def create_simulation_environment(self):
        """
        Create simulation environment to perform simulations using the pool of building energy models
        """
        self.weather_data = read_weather_data(self.weather_file, year=self.year, mapping=self.mapping, date_format=self.date_format, time_zone=self.time_zone)

    def run_parallel_simulation(self):
        """
        Run parallel building energy simulations.
        """
        for ddbem in self.pool:
            ddbem.weather_data = self.weather_data
            start_date = ddbem.get_start_date().replace(tzinfo=pytz.timezone(self.time_zone))
            end_date = ddbem.get_end_date().replace(tzinfo=pytz.timezone(self.time_zone))
            dt = ddbem.get_dt()
            ddbem.output_dir = self.output_dir
            ddbem.target = read_building_energy_data(os.path.join(self.building_energy_data_dir, ddbem.building.name +'.csv'), year=self.year, timezone=self.time_zone)
            if ddbem.training_split_ratio > 0.0:
                dsplit = int(ddbem.training_split_ratio * (end_date - start_date) / dt)
                split_date = start_date + dsplit * dt
                ddbem.train(start_date, split_date, dt)
                previous_error_building_load = ddbem.get_previous_error_building_load(start_date, split_date, dt)
                current_error_building_load = ddbem.get_current_error_building_load(start_date, split_date, dt)
                if previous_error_building_load < current_error_building_load:
                    ddbem.update_previous_solution()
                ddbem.test(split_date + dt, end_date, dt)
            else:
                with open(os.path.join(self.output_dir, ddbem.building.name + '_trained_parameters.json'), 'r') as f:
                    results = json.load(f)
                ddbem.current_lumped_thermal_parameters[0] = results['exterior_wall_thermal_capacitance']
                ddbem.current_lumped_thermal_parameters[1] = results['interior_wall_thermal_capacitance']
                ddbem.current_lumped_thermal_parameters[2] = results['internal_mass_thermal_capacitance']
                ddbem.current_lumped_thermal_parameters[3] = results['outdoor_air_exterior_wall_thermal_resistance']
                ddbem.current_lumped_thermal_parameters[4] = results['sky_exterior_wall_thermal_resistance']
                ddbem.current_lumped_thermal_parameters[5] = results['wall_interior_exterior_wall_thermal_resistance']
                ddbem.current_lumped_thermal_parameters[6] = results['indoor_air_interior_wall_thermal_resistance']
                ddbem.current_lumped_thermal_parameters[7] = results['internal_mass_interior_wall_thermal_resistance']
                ddbem.current_lumped_thermal_parameters[8] = results['indoor_air_internal_mass_thermal_resistance']
                ddbem.current_lumped_thermal_parameters[9] = results['fraction_direct_normal_radiation']
                ddbem.current_lumped_thermal_parameters[10] = results['fraction_diffuse_horizontal_radiation']
                ddbem.current_lumped_thermal_parameters[11] = results['indoor_air_outdoor_air_thermal_resistance']
                ddbem.current_lumped_thermal_parameters[12] = results['indoor_air_outdoor_air_mass_resistance']
                ddbem.test(start_date, end_date, dt)

    def get_building_outputs(self, building_name):
        """
        :param building_name: name of the building
        :return: outputs of the simulation for the building
        """
        building = None
        for ddbem in self.pool:
            if ddbem.building.name == building_name:
                building = ddbem.building
                start_date = ddbem.get_start_date().replace(tzinfo=pytz.timezone(self.time_zone))
                end_date = ddbem.get_end_date().replace(tzinfo=pytz.timezone(self.time_zone))
                dt = ddbem.get_dt()
                break
        data = {
            'Total sensible load': building.get_sensible_load().values,
            'Total latent load': building.get_latent_load().values,
            'Average walls surface temperature': building.get_walls_temperature().values
        }
        return pd.DataFrame(index=pd.date_range(start_date, end_date, freq=dt), data=data)

    def cleanup(self):
        """
        Cleanup the simulation environment.
        """
        pass

def read_building_energy_data(building_energy_data_file, year = date.today().year, timezone='GMT', type='eplus'):
    """
    Read building energy data.
    """
    if type == 'eplus':
        return EnergyPlusDataLoader(building_energy_data_file, year=year, timezone=timezone).load()

def read_weather_data(weather_file, year = date.today().year, mapping = {}, date_format = '%Y-%m-%d %H:%M:%S', time_zone='GMT'):
    """
    Read weather data to be used as boundary conditions of a building energy model.
    :param weather_file: file containing weather data.
    :param year: year during which weather data were collected.
    :param mapping: dictionary defining the correspondance of each
    :return: (WeatherData) weather data
    """
    filename, extension = os.path.splitext(weather_file)
    if extension == '.epw':
        weather_data_loader = EPWDataLoader(weather_file, year = year)
    elif extension == '.csv':
        weather_data_loader = CSVDataLoader(weather_file, mapping = mapping, date_format = date_format, time_zone=time_zone)
    return weather_data_loader.load()

def modify_weather_data(src, dst, output_file,
                        src_year = date.today().year, src_mapping = {}, src_date_format = '%Y-%m-%d %H:%M:%S', src_time_zone='GMT',
                        dst_year = date.today().year, dst_mapping = {}, dst_date_format = '%Y-%m-%d %H:%M:%S', dst_time_zone='GMT'):
    """
    Modify weather data contained in a source file with data stored in a destination file.
    :param src: source weather file.
    :param dst: destination weather file.
    """
    src_weather_data = read_weather_data(src, year = src_year, mapping = src_mapping, date_format=src_date_format, time_zone=src_time_zone)
    dst_weather_data = read_weather_data(dst, year = dst_year, mapping = dst_mapping, date_format=dst_date_format, time_zone=dst_time_zone)
    for k in dst_weather_data.keys():
        if k in src_weather_data.keys():
            src_weather_data[k] = dst_weather_data[k]
    src_weather_data.save(output_file)

def run_simulation(weather_file, type = 'eplus', year = date.today().year, time_zone='GMT',
                   input_dir = '.', output_dir = '.', building_energy_data_dir='.', tsr=0.0):
    """
    Run building energy simulation.
    :param weather_file: weather file used to perform the building energy simulation.
    :param year: year at which weather data must be expressed. Default is current year.
    :param input_dir: directory in which configuration files of building energy models are stored.
    :param output_dir: directory in which simulations are performed and output files are stored.
    :param type: type of building energy simulation ('eplus' or 'datadriven').
    """
    if type == 'eplus':
        bems_pool = EnergyPlusSimulationPool(weather_file, year = year)
        bems_pool.output_dir = output_dir
        all_files = os.listdir(input_dir)
        filtered_files = [f for f in all_files if f.endswith('.idf')]
        for f in filtered_files:
            bems_pool.pool.append(EnergyPlusModel(IDFBuildingLoader(os.path.join(input_dir, f))))
    elif type == 'datadriven':
        bems_pool = DataDrivenBuildingEnergySimulationPool(weather_file, building_energy_data_dir=building_energy_data_dir, output_dir=output_dir, year=year, time_zone=time_zone)
        all_files = os.listdir(input_dir)
        filtered_files = [f for f in all_files if f.endswith('.idf')]
        for f in filtered_files:
            bems_pool.pool.append(LinearStateSpaceBuildingEnergyModel(IDFBuildingLoader(os.path.join(input_dir, f)), training_split_ratio=tsr))
    bems_pool.run()

