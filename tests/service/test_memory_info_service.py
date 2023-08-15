import unittest

from assertpy import assert_that

from beholder.service.memory_info_service import MemoryInfoService


class TestMemoryInfoService(unittest.TestCase):
    def setUp(self) -> None:
        self.service: MemoryInfoService = MemoryInfoService()
        self.result: dict[str, any] = self.service.get_info()

    def test_physicalMemoryIsAvailable(self):
        assert_that(self.result).contains("physical_memory")

    def test_swapMemoryIsAvailable(self):
        assert_that(self.result).contains("swap_memory")

    def test_physicalMemoryTotalAvailableIsAvailable(self):
        assert_that(self.result["physical_memory"]).contains("total_available")
        assert_that(self.result["physical_memory"]["total_available"]).matches("[0-9\\.]*?B")

    def test_swapMemoryTotalAvailableIsAvailable(self):
        assert_that(self.result["swap_memory"]).contains("total_available")
        assert_that(self.result["swap_memory"]["total_available"]).matches("[0-9\\.]*?B")

    def test_physicalMemoryPctUsedIsAvailable(self):
        assert_that(self.result["physical_memory"]).contains("pct_used")
        assert_that(self.result["physical_memory"]["pct_used"]).is_greater_than(0.0)

    def test_swapMemoryPctUsedIsAvailable(self):
        assert_that(self.result["swap_memory"]).contains("pct_used")
        assert_that(self.result["swap_memory"]["pct_used"]).is_greater_than(0.0)

    def test_physicalMemoryTotalFreeIsAvailable(self):
        assert_that(self.result["physical_memory"]).contains("total_free")
        assert_that(self.result["physical_memory"]["total_free"]).matches("[0-9\\.]*?B")

    def test_swapMemoryTotalFreeIsAvailable(self):
        assert_that(self.result["swap_memory"]).contains("total_free")
        assert_that(self.result["swap_memory"]["total_free"]).matches("[0-9\\.]*?B")
