import os

import psutil

from ..service.info_service import InfoService


class ServiceInfoService(InfoService):
    """Info service implementation specialized to retrieve the status of services in the system."""

    # List of the services to be watched by the application.
    __service_watch_list: dict[str, bool] = {}

    def __init__(self):
        """Default class constructor. Initializes the service watch list based on the BEHOLDER_SERVICES_WATCHLIST
        environment variable, which should contains a coma separated list of all services to be watched by the
        application. If the environment variable is not available, an empty string is used by default.
        """
        services: list[str] = os.environ.get("BEHOLDER_SERVICES_WATCHLIST", "").strip().split(",")
        if len(services) > 0 and services[0] != "":
            self.__service_watch_list = {service: False for service in services}

    def get_info(self) -> dict[str, any]:
        """Retrieve, format and return the status of all the watched services. The returned dictionary has the service
        name and the entry key, and the service status as the entry value.

        :return: A dictionary with the aforementioned entries.
        """
        services_statuses: dict[str, any] = {}

        if len(self.__service_watch_list) > 0:
            services_statuses = self.__service_watch_list.copy()
            for process in psutil.process_iter():
                with process.oneshot():
                    if process.name() in services_statuses:
                        services_statuses[process.name()] = process.is_running()

        return services_statuses
