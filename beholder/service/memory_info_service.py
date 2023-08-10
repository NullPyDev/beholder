import psutil

from beholder.common.formatter import size_formatter
from ..service.info_service import InfoService


class MemoryInfoService(InfoService):
    """Infor service implementation specialized to retrieve details about the available memory and its usage."""

    # Retrieved memory details.
    __info: dict[str, any] = None

    def get_info(self) -> dict[str, any]:
        """Retrieve, formant and return details about the available memory and its current usage. The returned
        dictionary contains the following entries:

        * physical_memory: Dictionary containing the total available and the percentual used of the physical memory.
        * swap_memory: Dictionary containing the total available and the percentual used of the SWAP memory.

        :return: Dictionary containing the aforementioned entries.
        """
        if not self.__info:
            self.__info = {
                "physical_memory": {"total_available": size_formatter(psutil.virtual_memory().total)},
                "swap_memory": {"total_available": size_formatter(psutil.swap_memory().total)},
            }

        self.update_pct_used_for_memory(self.__info["physical_memory"], psutil.virtual_memory())
        self.update_pct_used_for_memory(self.__info["swap_memory"], psutil.swap_memory())
        return self.__info

    @staticmethod
    def update_pct_used_for_memory(memory_summary: dict[str, any], memory_info):
        memory_summary["pct_used"] = memory_info.percent
