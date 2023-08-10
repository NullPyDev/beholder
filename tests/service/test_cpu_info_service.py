import unittest

from assertpy import assert_that

from beholder.service.cpu_info_service import CPUInfoService


class TestCPUInfoService(unittest.TestCase):
    def setUp(self) -> None:
        self.service: CPUInfoService = CPUInfoService()
        self.result: dict[str, any] = self.service.get_info()

    def test_physicalCoresIsAvailable(self):
        assert_that(self.result).contains("physical_cores")
        assert_that(self.result["physical_cores"]).is_greater_than(0)

    def test_totalCoresIsAvailable(self):
        assert_that(self.result).contains("total_cores")
        assert_that(self.result["total_cores"]).is_greater_than(0)

    def test_maxFrequencyIsAvailable(self):
        assert_that(self.result).contains("max_frequency")
        assert_that(self.result["max_frequency"]).matches("[0-9\\.]*?hz")

    def test_currentFrequencyIsAvailable(self):
        assert_that(self.result).contains("current_frequency")
        assert_that(self.result["current_frequency"]).matches("[0-9\\.]*?hz")

    def test_pctCurrentFrequencyIsAvailable(self):
        assert_that(self.result).contains("pct_current_frequency")
        assert_that(self.result["pct_current_frequency"]).is_greater_than_or_equal_to(0)

    def test_totalLoadIsAvailable(self):
        assert_that(self.result).contains("total_load")
        assert_that(self.result["total_load"]).is_greater_than_or_equal_to(0)
