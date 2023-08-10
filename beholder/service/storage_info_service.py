import logging
from logging import Logger

import psutil

from ..common.formatter import size_formatter
from ..service.info_service import InfoService


class StorageInfoService(InfoService):
    """Info service implementation specialized to retrieve the details and usage statistics from all the storage
    devices available in the node.
    """

    # Local logger.
    __logger: Logger = None

    def __init__(self):
        """Default class constructor."""
        self.__logger = logging.getLogger(__name__)

    def get_info(self) -> dict[str, any]:
        """Retrieve, format and return details about all available storage devices and its usage. The returned
        dictionary contains the following entries:

        * device: Entry key.
        * total_size: Disk capacity.
        * total_free: Total space available in the disk.
        * pct_used: Used space expressed in percentage.

        :return: A dictionary containing the aforementioned entries.
        """
        disks: dict[str, any] = {}
        for partition in psutil.disk_partitions():
            if partition.device not in disks:
                try:
                    usage = psutil.disk_usage(partition.mountpoint)

                except PermissionError:
                    self.__logger.warning(
                        "It was not possible to retrieve usage statistics for the device '%s' "
                        "due the following error:",
                        partition.device,
                        exc_info=True,
                    )
                    continue

                disks[partition.device] = {
                    "total_size": size_formatter(usage.total),
                    "total_free": size_formatter(usage.free),
                    "pct_used": usage.percent,
                }

        return disks
