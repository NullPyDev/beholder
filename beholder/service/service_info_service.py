import os

import psutil

from ..service.info_service import InfoService


class ServiceInfoService(InfoService):
    """Info service implementation specialized to retrieve the status of services in the system."""

    # List of the services to be watched by the application.
    __service_watch_list: list[str] = None

    def __init__(self):
        """Default class constructor. Initializes the service watch list based on the BEHOLDER_SERVICES_WATCHLIST
        environment variable, which should contains a coma separated list of all services to be watched by the
        application. If the environment variable is not available, an empty string is used by default.
        """
        self.__service_watch_list = os.environ.get("BEHOLDER_SERVICES_WATCHLIST", "").strip().split(",")

    def get_info(self) -> dict[str, any]:
        """Retrieve, format and return the status of all the watched services. The returned dictionary has the service
        name and the entry key, and the service status as the entry value.

        :return: A dictionary with the aforementioned entries.
        """
        services_statuses: dict[str, any] = {}

        for process in psutil.process_iter():
            with process.oneshot():
                if process.name() in self.__service_watch_list:
                    services_statuses[process.name()] = process.is_running()

        for watched_service in self.__service_watch_list:
            if watched_service not in services_statuses and watched_service != "":
                services_statuses[watched_service] = False

        return services_statuses
