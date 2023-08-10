import unittest

from assertpy import assert_that

from beholder.facade.dashboard_facade import DashboardFacade


class TestDashboardFacade(unittest.TestCase):

    def setUp(self) -> None:
        self.facade: DashboardFacade = DashboardFacade()
        self.result: dict[str, any] = self.facade.load_summaries()

    def test_sysInfoIsAvailable(self):
        assert_that(self.result).contains("sys_info")

    def test_cpuInfoIsAvailable(self):
        assert_that(self.result).contains("cpu_info")

    def test_memInfoIsAvailable(self):
        assert_that(self.result).contains("mem_info")

    def test_storageInfoIsAvailable(self):
        assert_that(self.result).contains("storage_info")

    def test_servicesInfoIsAvailable(self):
        assert_that(self.result).contains("services_info")

    def test_networkInfoIsAvailable(self):
        assert_that(self.result).contains("network_info")

    def test_temperatureInfoIsAvailable(self):
        assert_that(self.result).contains("temperature_info")
