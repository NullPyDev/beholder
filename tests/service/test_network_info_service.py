import unittest

from assertpy import assert_that

from beholder.service.network_info_service import NetworkInfoService


class TestNetworkInfoService(unittest.TestCase):

    def setUp(self) -> None:
        self.service: NetworkInfoService = NetworkInfoService()
        self.result: dict[str, any] = self.service.get_info()

    def test_loopBackInterfaceIsNotListed(self):
        assert_that(self.result).does_not_contain("lo")

    def test_availableInterfacesHaveStatus(self):
        for interface, details in self.result.items():
            assert_that(details).contains("active")
            assert_that(details["active"]).is_type_of(bool)

    def test_availableInterfacesHaveAddresses(self):
        for interface, details in self.result.items():
            assert_that(details).contains("addresses")
            assert_that(details["addresses"]).is_not_empty()

    def test_forEachInterfaceAddressThereIsOneAddressAvailable(self):
        for interface, details in self.result.items():
            for address in details["addresses"]:
                assert_that(address).contains("address")
                assert_that(address).contains("address_type")
