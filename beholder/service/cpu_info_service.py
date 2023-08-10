import psutil

from ..common.formatter import frequency_formatter
from ..service.info_service import InfoService


class CPUInfoService(InfoService):
    """Info service implementation specialized to retrieve details about the system CPU and its usage."""

    # Retrieved CPU details.
    __info: dict[str, any] = None

    def get_info(self) -> dict[str, any]:
        """Retrieve, format and return details about the installed CPU and its current load. The returned dictionary
        contains the following entries:

        * physical_cores: Number of available physical cores. Retrieved just once.
        * total_cores: Number of available physical and local cores. Retrieved just once.
        * max_frequency: Maximum CPU frequency. Retrieved just once.
        * current_frequency: Current CPU frequency.
        * pct_current_frequency: Percentage of the current CPU frequency in relation to the maximum CPU frequency.
        * total_load: Total loaded applied to the CPU expressed as percentage.

        :return: A dictionary containing the aforementioned entries.
        """
        if not self.__info:
            self.__info = {
                "physical_cores": psutil.cpu_count(logical=False),
                "total_cores": psutil.cpu_count(logical=True),
                "max_frequency": frequency_formatter(psutil.cpu_freq().max),
            }
        self.__info["current_frequency"] = frequency_formatter(psutil.cpu_freq().current)
        self.__info["pct_current_frequency"] = (psutil.cpu_freq().current / psutil.cpu_freq().max) * 100
        self.__info["total_load"] = psutil.cpu_percent()
        return self.__info
