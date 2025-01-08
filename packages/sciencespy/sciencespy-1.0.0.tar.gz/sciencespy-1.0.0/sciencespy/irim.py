"""
Module to extract and process thermal images collected from an IR camera.

Delft University of Technology
Dr. Miguel Martin
"""

from abc import ABCMeta, abstractmethod

import os
import math
import datetime
import time
import calendar
import re
import numpy as np
import pandas as pd
from fnv.file import ImagerFile
import h5py
import bisect
import PIL.Image



class ThermalImages:
    """
    Class representing a series of thermal images collected from an IR camera.

    Attributs:
        index: index representing the time at which each thermal image was taken.
        images: corresponding thermal images taken at each time specified in the index.
    """

    def __init__(self, index = [], images = []):
        """
        :param index: index representing the time at which each thermal image was taken.
        :param images: corresponding thermal images taken at each time specified in the index.
        """
        sorted_index = sorted(enumerate(index), key=lambda x: x[1])
        self.index = [item[1] for item in sorted_index]
        self.images = [images[item[0]] for item in sorted_index]

    def __getitem__(self, index):
        """
        :param index: index representing the time at which a thermal image was obtained.
        :return: the corresponding thermal image as a numpy array.
        """
        return self.images[self.index.index(index)]

    def __setitem__(self, index, image):
        """
        :param index: index representing the time at which a thermal image was obtained.
        :param image: the corresponding thermal image as a numpy array.
        """
        if index not in self.index:
            n = bisect.bisect_left(self.index, index)
            self.index.insert(n, index)
            self.images.insert(n, image)
        else:
            self.images[self.index.index(index)] = image

    def __len__(self):
        return len(self.index)

    def append(self, other):
        """
        Append indexes and images to the existing series.
        :param other: series of thermal images to append.
        """
        for n in range(len(other)):
            self.__setitem__(other.index[n], other.images[n])

    def iterator(self):
        """
        Iterate over the sequence of thermal images.
        """
        for index, image in zip(self.index, self.images):
            yield index, image

    def get_thermal_properties(self, label_folder):
        """
        Get thermal properties of elements specified using the software Labelme (https://github.com/wkentaro/labelme)

        :param label_folder: folder in which label images and names are stored.
        :return: DataFrame containing the thermal properties of each element specified by the label images
        """
        with open(os.path.join(label_folder, 'label_names.txt')) as file:
            label_names = [line.strip() for line in file.readlines()]
        label_array = np.asarray(PIL.Image.open(os.path.join(label_folder, 'label.png')))
        df = pd.DataFrame(index=pd.DatetimeIndex(self.index), columns=label_names)
        df.index.name = 'Timestamp'
        for dt in self.index:
            for ln in range(len(label_names)):
                mask = (label_array == ln).astype(float)
                mask[mask == 0] = np.nan
                df.loc[dt.strftime('%Y-%m-%d %H:%M:%S'), label_names[ln]] = np.nanmean(mask * self.__getitem__(dt))
        return df.drop(columns=['_background_'], inplace=False)

class ThermalImagesLoader():
    """
    Class to load thermal images captured by a thermal camera.

    Attributes:
        image_file: file in which one or several thermal images are stored.
        operation: operation made on thermal images (e.g. none, avg, or median)
        must_convert_to_thermal: True if the radiometric values of the image are converted to thermal.
    """
    __metaclass__ = ABCMeta

    def __init__(self, image_file, operation='none', must_convert_to_thermal=False):
        """
        :param image_file: file in which one or several thermal images are stored.
        :param operation: operation made on thermal images (e.g. none, avg, or median).
        :param must_convert_to_thermal: True if the radiometric values of images are converted to thermal.
        """
        self.image_file = image_file
        self.operation = operation
        self.must_convert_to_thermal = must_convert_to_thermal

    def load(self):
        """"
        Load the thermal image.
        :return: loaded thermal image
        """
        index, array_images = self.read_radiometric_images(self.image_file)
        if self.operation == 'avg':
            return ThermalImages(index=[index[0]], images=[np.average(array_images, axis=2)])
        elif self.operation == 'median':
            return ThermalImages(index=[index[0]], images=[np.median(array_images, axis=2)])
        else:
            return ThermalImages(index=index, images=[array_images[:, :, r] for r in range(array_images.shape[2])])

    @abstractmethod
    def read_radiometric_images(self, image_file):
        """
        :param image_file: file in which one or several radiometric images are stored.
        :return: list of radiometric images and their datetime index.
        """
        pass

class FLIRImagesLoader(ThermalImagesLoader):
    """
    Class to load thermal images captured by a FLIR thermal camera.

    Attributes:
        image_file: file in which one or several thermal images are stored.
        operation: operation made on thermal images (e.g. none, avg, or median)
        must_convert_to_thermal: True if the radiometric values of the image are converted to thermal.
        emissivity_matrix: matrix for emissivity of each surface observed by the thermal camera (0-1)
        distance_matrix: matrix for distance between each surface and the thermal camera (in meter)
        outdoor_air_temperature: outdoor air temperature (in degree Celsius)
        outdoor_air_humidity: outdoor air humidity (in percent)
        sky_temperature: sky temperature (in degree Celsius)
        calibration_parameters: calibration parameters for the thermal camera.
    """

    __metaclass__ = ABCMeta

    def __init__(self, image_file, operation='none'):
        """
        :param image_file: file in which one or several thermal images are stored.
        :param operation: operation made on thermal images (e.g. none, avg, or median)
        """
        ThermalImagesLoader.__init__(self, image_file, operation)


class FLIRSEQImagesLoader(ThermalImagesLoader):
    """
    Class to load thermal images captured by a FLIR thermal camera using the SEQ format.

    Attributes:
        image_file: file in which the thermal image is stored.
        operation: operation made on thermal images (e.g. none, avg, or median)
    """

    def __init__(self, image_file, operation='none'):
        """
        :param image_file: file in which one or several thermal images are stored.
        :param operation: operation made on thermal images (e.g. none, avg, or median)
        """
        ThermalImagesLoader.__init__(self, image_file, operation)

    def read_radiometric_images(self, image_file):
        """
        :param image_file: file in which the radiometric image is stored.
        :return: list of radiometric images and their datetime index.
        """
        seq_file = ImagerFile(image_file)
        index = []
        images = np.zeros((seq_file.height, seq_file.width, seq_file.num_frames))
        for i in range(seq_file.num_frames):
            seq_file.get_frame(i)
            index.append(seq_file.frame_info.time)
            images[:, :, i] = np.array(seq_file.final).reshape(seq_file.height, seq_file.width)
        return index, images


def extract_thermal_images(image_dir='.', operation='none'):
    """
    Extract thermal images stored in a directory.
    :param image_dir: directory in which thermal images are stored.
    :param operation: operation to apply on a sequence of thermal images (if needed)
    """
    thermal_images = ThermalImages()
    files = [f for f in os.listdir(image_dir) if os.path.isfile(os.path.join(image_dir, f))]
    for f in files:
        filename, ext = os.path.splitext(f)
        if ext == '.seq':
            print('--> Loading thermal image ' + f + ' ...')
            loader = FLIRSEQImagesLoader(os.path.join(image_dir, f), operation=operation)
        thermal_images.append(loader.load())
    return thermal_images

class RadiometricToTemperatureConverter():
    """
    Class to convert a radiometric value or image to a temperature value, timeseries, or image.

    Attributes:
        emissivity: emissivity of the target surface (0-1).
        distance: distance between the target surface and the thermal camera (in meters).
        outdoor_temperature: outdoor temperature at the moment the value or image was taken by the thermal camera (in degree Celsius)
        outdoor_humidity: outdoor humidity at the moment the value or image was taken by the thermal camera (in percentage)
        sky_temperature: sky temperature at the moment the value or image was taken by the thermal camera (in degree Celsius)
    """
    __metaclass__ = ABCMeta

    def __init__(self, emissivity, distance, outdoor_temperature=25.0, outdoor_humidity=50.0, sky_temperature=20.0):
        """
        :param emissivity: emissivity of the target surface (0-1).
        :param distance: distance between the target surface and the thermal camera (in meters)
        :param outdoor_temperature: outdoor temperature at the moment the value or image was taken by the thermal camera (in degree Celsius)
        :param outdoor_humidity: outdoor humidity at the moment the value or image was taken by the thermal camera (in percentage)
        :param sky_temperature: sky temperature at the moment the value or image was taken by the thermal camera (in degree Celsius)
        """
        self.emissivity = emissivity
        self.distance = distance
        self.outdoor_temperature = outdoor_temperature
        self.outdoor_humidity = outdoor_humidity
        self.sky_temperature = sky_temperature

    def convert(self, timestamps, radiometric_values):
        """
        Convert the radiometric values to temperature (in degree Celsius)
        :param timestamps: timestamps at which each radiometric value was collected.
        :param radiometric_values: radiometric values to be converted.
        :return: converted radiometric values (in degree Celsius)
        """
        temperature_values = np.zeros(len(timestamps))
        for n, timestamp in enumerate(timestamps):
            Tout = self.outdoor_temperature if isinstance(self.outdoor_temperature, float) else self.outdoor_temperature.reindex(self.outdoor_temperature.index.union([timestamp]).sort_values()).interpolate(method='time').loc[timestamp]
            RH = self.outdoor_humidity if isinstance(self.outdoor_humidity, float) else self.outdoor_humidity.reindex(self.outdoor_humidity.index.union([timestamp]).sort_values()).interpolate(method='time').loc[timestamp]
            Tsky = self.sky_temperature if isinstance(self.sky_temperature, float) else self.sky_temperature.reindex(self.sky_temperature.index.union([timestamp]).sort_values()).interpolate(method='time').loc[timestamp]

            h1 = 6.8455e-7
            h2 = -2.7816e-4
            h3 = 6.939e-2
            h4 = 1.5587
            water_vapour_content = (RH / 100.0) * math.exp(h1 * Tout ** 3 + h2 * Tout ** 2 + h3 * Tout + h4)
            x = 1.9
            a1 = 0.0066
            a2 = 0.0126
            b1 = -0.0023
            b2 = -0.0067
            atmospheric_transmissivity = x * math.exp(- math.sqrt(self.distance) * (a1 + b1 * math.sqrt(water_vapour_content))) + (1 - x) * math.exp(- math.sqrt(self.distance) * (a2 + b2 * math.sqrt(water_vapour_content)))

            temp2rad = self.func_temp2rad()
            radiometric_outdoor_temperature = temp2rad(Tout)
            radiometric_sky_temperature = temp2rad(Tsky)

            K1 = 1 / (self.emissivity * atmospheric_transmissivity)
            r1 = ((1 - self.emissivity) / self.emissivity) * radiometric_sky_temperature
            r2 = ((1 - atmospheric_transmissivity) / (self.emissivity * atmospheric_transmissivity)) * radiometric_outdoor_temperature
            K2 = r1 + r2
            true_radiometric_image = K1 * float(radiometric_values[n]) - K2
            rad2temp = self.func_rad2temp()
            temperature_values[n] = rad2temp(true_radiometric_image)
        return temperature_values

    @abstractmethod
    def func_temp2rad(self):
        """
        :return: function used to convert a value expressed in temperature to radiometric.
        """
        pass

    @abstractmethod
    def func_rad2temp(self):
        """
        :return: function used to convert a value expressed in radiometric to temperature.
        """
        pass

class FLIRRadiometricToTemperatureConverter(RadiometricToTemperatureConverter):
    """
    Class to convert a radiometric value or image to a temperature value or image taken from a FLIR camera.

    Attributes:
        radiometric: value or image expressed in radiometric.
        timestamp: date and time at which the value or image was collected by the thermal camera.
        emissivity: emissivity of the target surface (0-1).
        distance: distance between the target surface and the thermal camera (in meters).
        outdoor_temperature: outdoor temperature at the moment the value or image was taken by the thermal camera (in degree Celsius)
        outdoor_humidity: outdoor humidity at the moment the value or image was taken by the thermal camera (in percentage)
        sky_temperature: sky temperature at the moment the value or image was taken by the thermal camera (in degree Celsius)
        R: first calibration parameter.
        B: second calibration parameter.
        F: third calibration parameter.
        J1: fourth calibration parameter.
        J0: fifth calibration parameter.
    """

    def __init__(self, emissivity, distance, outdoor_temperature=25.0, outdoor_humidity=50.0, sky_temperature=20.0,
                 R = 14911.1846, B = 1396.6, F = 1.0, J1 = 0.0108, J0 = -1000.0):
        """
        :param emissivity: emissivity of the target surface (0-1).
        :param distance: distance between the target surface and the thermal camera (in meters)
        :param outdoor_temperature: outdoor temperature at the moment the value or image was taken by the thermal camera (in degree Celsius)
        :param outdoor_humidity: outdoor humidity at the moment the value or image was taken by the thermal camera (in percentage)
        :param sky_temperature: sky temperature at the moment the value or image was taken by the thermal camera (in degree Celsius)
        :param R: first calibration parameter.
        :param B: second calibration parameter.
        :param F: third calibration parameter.
        :param J1: fourth calibration parameter.
        :param J0: fifth calibration parameter.
        """
        RadiometricToTemperatureConverter.__init__(self, emissivity, distance, outdoor_temperature, outdoor_humidity, sky_temperature)
        self.R = R
        self.B = B
        self.F = F
        self.J1 = J1
        self.J0 = J0

    def func_temp2rad(self):
        """
        :return: function used to convert a value expressed in temperature to radiometric.
        """
        return lambda T : (self.R / (self.J1 * ((math.exp(self.B / (T + 273.15)) - self.F)))) - self.J0

    def func_rad2temp(self):
        """
        :return: function used to convert a value expressed in radiometric to temperature.
        """
        return lambda I : (self.B / math.log((self.R / (self.J1 * (I + self.J0))) + self.F)) - 273.15

def convert_radiometric_values(dataframe, emissivity_objects, distance_objects, outdoor_temperature=25.0, outdoor_humidity=50.0, sky_temperature=20.0,
                               converter_name='flir', R = 14911.1846, B = 1396.6, F = 1.0, J1 = 0.0108, J0 = -1000.0):
    """
    Convert radiometric values of each object stored in a dataframe.
    :param dataframe: dataframe in which radiometric values of each object are stored.
    :param emissivity_objects: emissivity of each object stored in the dataframe.
    :param distance_objects: distance of each object from the infrared camera.
    :param outdoor_temperature: outdoor temperature when radiometric values were collected.
    :param outdoor_humidity: outdoor humidity when radiometric values were collected.
    :param sky_temperature: sky temperature when radiometric values were collected.
    :param converter_name: name of converter to temperature values (in degree Celsius)
    :param R, B, F, J1, and J0: calibration parameters of the FLIR camera.
    """
    name_objects = dataframe.columns.tolist()
    new_dataframe = pd.DataFrame(index=dataframe.index, columns=name_objects)
    for nobj, name_obj in enumerate(name_objects):
        if converter_name == 'flir':
            converter = FLIRRadiometricToTemperatureConverter(emissivity_objects[nobj],
                                                              distance_objects[nobj],
                                                              outdoor_temperature=outdoor_temperature,
                                                              outdoor_humidity=outdoor_humidity,
                                                              sky_temperature=sky_temperature,
                                                              R = R, B = B, F = F, J1 = J1, J0 = J0)
        new_dataframe[name_obj] = converter.convert(timestamps=dataframe.index, radiometric_values=dataframe[name_obj].values)
    return new_dataframe