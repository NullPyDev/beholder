import psutil
from psutil._common import snicaddr, snicstats

from ..service.info_service import InfoService


class NetworkInfoService(InfoService):
    """Info service implementation specialized to retrieved details and statistics about the network interfaces
    available in the system.
    """

    def get_info(self) -> dict[str, any]:
        """Retrieve, format and return details about the available network interfaces in the system. The returned
        dictionary contains the following entries:

        * interface_name: Dictionary entry key.
        * active: A boolean flag indicating if the interface is active (True) or not (False).
        * addresses: A list of dictionary containing the addresses assigned to the interface, which has the
        following entries:
            * address: Address assigned to the interface.
            * address_type: Type of the address assigned to the interface (E.g. IP, IPv6, MAC).

        The loopback interface is intentionally removed from the list for the simplicity sake.

        :return: A dictionary containing the aforementioned entries.
        """
        if_summaries: dict[str, any] = {}
        if_addresses: dict[str, list[snicaddr]] = psutil.net_if_addrs()
        if_statuses: dict[str, snicstats] = psutil.net_if_stats()

        for interface, addresses in if_addresses.items():
            if interface != "lo":
                if_summaries[interface] = {
                    "active": if_statuses[interface][0],
                    "addresses": self.load_interface_addresses(addresses),
                }

        return if_summaries

    @staticmethod
    def load_interface_addresses(addresses: list[snicaddr]) -> list[dict[str, any]]:
        """Retrieve the addresses assigned to the network interface. Each dictionary in the list contains the following
        entries:

        * address: Address assigned to the interface.
        * address_type: Type of the address assigned to the interface (E.g. IP, IPv6, MAC).

        :param addresses: Addresses assigned to the network interface.
        :return: A list of dictionaries containing the aforementioned entries.
        """
        address_summaries: list[dict[str, any]] = []
        for address in addresses:
            address_summaries.append({"address": address.address.split("%")[0], "address_type": address.family.name})
        return address_summaries
