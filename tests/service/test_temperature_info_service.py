import os
import unittest

from assertpy import assert_that

from beholder.service.temperature_info_service import TemperatureInfoService


class TestTemperatureInfoServiceWithCelsius(unittest.TestCase):

    def setUp(self) -> None:
        self.service: TemperatureInfoService = TemperatureInfoService()
        self.result: dict[str, any] = self.service.get_info()

    def test_sensorNameIsAvailable(self):
        assert_that(self.result.keys()).is_not_empty()

    def test_eachSensorHasAtLeastOneLabel(self):
        for sensor, readings in self.result.items():
            for reading in readings:
                assert_that(reading).contains("sensor_label")

    def test_scaleIsSetToCelsiusByDefault(self):
        for sensor, readings in self.result.items():
            for reading in readings:
                assert_that(reading["scale"]).is_equal_to("C")

    def test_eachSensorHasTheCurrentTemperature(self):
        for sensor, readings in self.result.items():
            for reading in readings:
                assert_that(reading).contains("temperature")

    def test_eachSensorHasLowBand(self):
        for sensor, readings in self.result.items():
            for reading in readings:
                assert_that(reading).contains("low_band")

    def test_eachSensorHasMediumBand(self):
        for sensor, readings in self.result.items():
            for reading in readings:
                assert_that(reading).contains("medium_band")

    def test_eachSensorHasHighBand(self):
        for sensor, readings in self.result.items():
            for reading in readings:
                assert_that(reading).contains("high_band")


class TestTemperatureInfoServiceWithFahrenheitScale(unittest.TestCase):

    def setUp(self) -> None:
        os.environ["BEHOLDER_TEMPERATURE_SCALE"] = "F"
        self.service: TemperatureInfoService = TemperatureInfoService()
        self.result: dict[str, any] = self.service.get_info()
        del os.environ["BEHOLDER_TEMPERATURE_SCALE"]

    def test_eachSensorHasFahrenheitAsScale(self):
        for sensor, readings in self.result.items():
            for reading in readings:
                assert_that(reading["scale"]).is_equal_to("F")
