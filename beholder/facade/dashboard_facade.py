from ..service.cpu_info_service import CPUInfoService
from ..service.info_service import InfoService
from ..service.memory_info_service import MemoryInfoService
from ..service.network_info_service import NetworkInfoService
from ..service.service_info_service import ServiceInfoService
from ..service.storage_info_service import StorageInfoService
from ..service.system_info_service import SystemInfoService
from ..service.temperature_info_service import TemperatureInfoService


class DashboardFacade:
    """Provide a single point to retrieve and gather all the required information to compose the system dashboard."""

    # Info service used to retrieve basic node information.
    __sys_info_service: InfoService = None

    # Info service used to retrieve CPU information and usage statistics.
    __cpu_info_service: InfoService = None

    # Info service used to retrieve memory information and usage statistics.
    __mem_info_service: InfoService = None

    # Info service used to retrieve storage information and usage statistics.
    __storage_info_service: InfoService = None

    # Info service used to retrieve watched services state.
    __services_info_service: InfoService = None

    # Info service used to retrieve network information, statistics and state.
    __network_info_service: InfoService = None

    # Info service used to retrieve the temperature readings from all the available sensors in the system.
    __temperature_info_service: InfoService = None

    def __init__(self):
        """Default class constructor. Instantiate all the required infor services used to gather the dashboard
        information.
        """
        self.__sys_info_service = SystemInfoService()
        self.__cpu_info_service = CPUInfoService()
        self.__mem_info_service = MemoryInfoService()
        self.__storage_info_service = StorageInfoService()
        self.__services_info_service = ServiceInfoService()
        self.__network_info_service = NetworkInfoService()
        self.__temperature_info_service = TemperatureInfoService()

    def load_summaries(self) -> dict[str, any]:
        """Retrieve and return the following system summaries:

        * sys_info: Basic system information retrieved using the :class:`SystemInfoService`.
        * cpu_info: CPU information and statistics, retrieved using the :class:`CPUInfoService`.
        * mem_info: Memory information and statistics, retrieved using the :class:`MemoryInfoService`.
        * storage_info: Storage information and statistics, retrieved using the :class:`StorageInfoService`.
        * services_info: Watched services statuses, retrieved using the :class:`ServiceInfoService`.
        * network_info: Network interfaces information and statistics, retrieved using the :class:`NetworkInfoService`.
        * temperature_info: Temperature readings retrieved from available sensors, retrieved using the
        :class:`TemperatureInfoService`

        :return: A dictionary filled with the aforementioned summaries. Please refer to each info service documentation
        for a proper description of its structure.
        """
        summaries: dict[str, any] = {
            "sys_info": self.__sys_info_service.get_info(),
            "cpu_info": self.__cpu_info_service.get_info(),
            "mem_info": self.__mem_info_service.get_info(),
            "storage_info": self.__storage_info_service.get_info(),
            "services_info": self.__services_info_service.get_info(),
            "network_info": self.__network_info_service.get_info(),
            "temperature_info": self.__temperature_info_service.get_info(),
        }
        return summaries
