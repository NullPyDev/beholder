import logging
import os
import subprocess
from logging import Logger

from ..service.info_service import InfoService


class ServiceInfoService(InfoService):
    """Info service implementation specialized to retrieve the status of services in the system."""

    # Local logger.
    __logger: Logger = None

    # List of the services to be watched by the application.
    __service_watch_list: list[str] = None

    def __init__(self):
        """Default class constructor. Initializes the service watch list based on the BEHOLDER_SERVICES_WATCHLIST
        environment variable, which should contains a coma separated list of all services to be watched by the
        application. If the environment variable is not available, an empty string is used by default.
        """
        self.__logger = logging.getLogger(__name__)
        self.__service_watch_list = os.environ.get("BEHOLDER_SERVICES_WATCHLIST", "").strip().split(",")

    def get_info(self) -> dict[str, any]:
        """Retrieve, format and return the status of all the watched services. The returned dictionary has the service
        name and the entry key, and the service status as the entry value.

        :return: A dictionary with the aforementioned entries.
        """
        services_statuses: dict[str, any] = {}

        for service_name in self.__service_watch_list:
            real_service_name = self.get_service_name(watch_list_entry=service_name)

            if len(real_service_name) > 0:
                status: bool = self.is_service_active(
                    service_name.strip().replace("&&", "").replace(">", "").replace("<", "").replace("|", "").split(" ")
                )
                services_statuses[real_service_name] = status

        return services_statuses

    def is_service_active(self, service_name) -> bool:
        """Invoke the systemctl command to retrieve the status of the service with the received name.

        :param service_name: Name of the service to have its status checked.
        :return: True if the service is active. Otherwise, False.
        """
        process = subprocess.Popen(["systemctl", "is-active", *service_name], stdout=subprocess.PIPE)

        try:
            output, err = process.communicate()
            if err:
                self.__logger.warning(
                    "The following error occurred when trying to probe the status of service '%s' using 'systemctl':",
                    str(service_name), str(err)
                )
                return False

        except Exception:
            self.__logger.warning(
                "It was not possible to probe the status of service '%s' using 'systemctl' due the following error:",
                str(service_name), exc_info=True
            )
            return False

        return output.decode("utf-8").replace("\n", "") == "active"

    @staticmethod
    def get_service_name(watch_list_entry: str) -> str:
        """Extract the proper name of the service being probed. Because the service name accepts flags like "--user",
        this value tries to split those values based on space and returns the very last piece of the resulting array.

        :param watch_list_entry: Entry of the services watching list.
        :return: The proper name to identify the service being probed.
        """
        real_service_name = watch_list_entry.strip().split(" ")
        return real_service_name[-1]
