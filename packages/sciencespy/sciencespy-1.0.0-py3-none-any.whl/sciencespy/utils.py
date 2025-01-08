"""
Module containing utility classes and functions used throughout the SCIENCES project.

Delft University of Technology
Dr. Miguel Martin
"""

from abc import ABCMeta, abstractmethod
import numpy as np
from sklearn.metrics import mean_squared_error
import pandas as pd

from pint import UnitRegistry
ureg = UnitRegistry()
ureg.define('percent = 1 / 100')

class ErrorFunction():
    """
    Class with which the error between two numerical vectors can be calculated.
    """
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_name(self):
        """
        :return: name of the error function.
        """
        pass

    @abstractmethod
    def err(self, vec1, vec2):
        """
        :param vec1: first numerical vector.
        :param vec2: second numerical vector.
        :return: error between two numerical vectors.
        """
        pass

class RootMeanSquareError(ErrorFunction):

    def get_name(self):
        """
        :return: name of the error function.
        """
        return 'RMSE'

    def err(self, vec1, vec2):
        """
        :param vec1: first numerical vector.
        :param vec2: second numerical vector.
        :return: error between two numerical vectors.
        """
        return np.sqrt(mean_squared_error(vec1, vec2))

class MeanBiasError(ErrorFunction):

    def get_name(self):
        """
        :return: name of the error function.
        """
        return 'MBE'

    def err(self, vec1, vec2):
        """
        :param vec1: first numerical vector.
        :param vec2: second numerical vector.
        :return: error between two numerical vectors.
        """
        return np.sum(vec1 - vec2) / len(vec1)

class CoefficientOfVariationOfRootMeanSquareError(RootMeanSquareError):

    def get_name(self):
        """
        :return: name of the error function.
        """
        return 'CV' + RootMeanSquareError.get_name(self)

    def err(self, vec1, vec2):
        """
        :param vec1: first numerical vector.
        :param vec2: second numerical vector.
        :return: error between two numerical vectors.
        """
        RMSE = RootMeanSquareError.err(self, vec1, vec2)
        return 100 * (RMSE / np.mean(vec2))

class NormalizeMeanBiasError(ErrorFunction):

    def get_name(self):
        """
        :return: name of the error function.
        """
        return "NMBE"

    def err(self, vec1, vec2):
        """
        :param vec1: first numerical vector.
        :param vec2: second numerical vector.
        :return: error between two numerical vectors.
        """
        return 100 * (np.mean(vec1) - np.mean(vec2)) / np.mean(vec2)

class QSeries(pd.Series):

    def __init__(self, index, data):
        pd.Series.__init__(self, index=index, data=data)
        self.data = data

def specific_humidity(temperature, relative_humidity, pressure):
    """
    :param temperature: temperature
    :param relative_humidity: relative humidity
    :param pressure: pressure
    :return: specific humidity (in kg/kg)
    """
    temp_degC = np.array([T.to('degC').m for T in temperature])
    relhum = np.array([(RH / 100).m for RH in relative_humidity])
    press_hPa = np.array([P.to('hPa').m for P in pressure])
    saturation_vapor_pressure = 6.112 * np.exp(np.divide(17.67 * temp_degC, temp_degC + 243.5))
    return 0.622 * np.divide(saturation_vapor_pressure, press_hPa) * relhum * (ureg.kilogram / ureg.kilogram)