import os

import psutil
from psutil._common import shwtemp

from ..service.info_service import InfoService


class TemperatureInfoService(InfoService):
    """Info service implementation specialized to retrieve the temperature reading of all available sensors."""

    # Temperature scale to be used (C or F)
    __temp_scale: str = None

    def __init__(self):
        """Default class constructor. Initializes the property with the temperature scale to be used, by reading from
        the BEHOLDER_TEMPERATURE_SCALE environment variable. If this variable is not available, Celsius (C) is used by
        default.
        """
        self.__temp_scale = os.environ.get("BEHOLDER_TEMPERATURE_SCALE", "C").strip().upper()

    def get_info(self) -> dict[str, any]:
        """Retrieve, format and return de temperature readings for each available sensor. The returned dictionary
        contains the following entries:

        * sensor_name: Entry key.
        * sensor_label: Label assigned to the sensor.
        * scale: Temperature scale used.
        * temperature: Current temperature reading.
        * low_band: Final temperature of the thermal lower band. It is calculated as 50% of the high temperature.
        * medium_band: Final temperature of the thermal medium band. It is calculated as 75% of the high temperature.
        * high_band: Final temperature of the thermal high band. It is the high temperature.

        :return: A dictionary containing the aforementioned entries.
        """
        sensor_readings: dict[str, any] = {}
        use_fahrenheit: bool = self.__temp_scale == "F"
        temp_readings: dict[str, list[shwtemp]] = psutil.sensors_temperatures(fahrenheit=use_fahrenheit)

        for sensor_name, temperatures in temp_readings.items():
            readings: list[dict[str, any]] = []

            for temperature in temperatures:
                high = 0.0

                # Workaround for some sensor with wrong temperature values for high.
                if temperature.high:
                    if temperature.high > 1_000:
                        high = temperature.high / 1_000
                    elif temperature.high > 100:
                        high = temperature.high / 100
                    else:
                        high = temperature.high

                readings.append(
                    {
                        "sensor_label": temperature.label,
                        "scale": self.__temp_scale,
                        "temperature": temperature.current,
                        "low_band": high * 0.5 if temperature.high else 0.0,
                        "medium_band": high * 0.75 if temperature.high else 0.0,
                        "high_band": high if temperature.high else 0.0,
                    }
                )

            sensor_readings[sensor_name] = readings

        return sensor_readings
