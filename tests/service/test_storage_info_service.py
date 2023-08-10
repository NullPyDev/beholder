import unittest
from unittest.mock import patch

from assertpy import assert_that

from beholder.service.storage_info_service import StorageInfoService


class TestStorageInfoService(unittest.TestCase):

    def setUp(self) -> None:
        self.service: StorageInfoService = StorageInfoService()
        self.result: dict[str, any] = self.service.get_info()

    def test_resultIsNotEmpty(self):
        assert_that(self.result).is_not_empty()

    def test_eachDeviceHasTotalSize(self):
        for device, info in self.result.items():
            assert_that(info).contains_key("total_size")
            assert_that(info["total_size"]).matches("[0-9\\.]*\\s?B")

    def test_eachDeviceHastTotalFree(self):
        for device, info in self.result.items():
            assert_that(info).contains("total_free")
            assert_that(info["total_free"]).matches("[0-9\\.]*\\s?B")

    def test_eachDeviceHasPctUsed(self):
        for device, info in self.result.items():
            assert_that(info).contains("pct_used")
            assert_that(info["pct_used"]).is_type_of(float)


class TestFailSilently(unittest.TestCase):

    def setUp(self) -> None:
        self.service: StorageInfoService = StorageInfoService()

    @patch("psutil.disk_usage", autospec=True)
    def test_failSilentlyWithException(self, mock_disk_usage):
        mock_disk_usage.side_effect = PermissionError("Fake Error")

        result: dict[str, any] = self.service.get_info()

        assert_that(result).is_not_none()
        assert_that(result).is_empty()
        mock_disk_usage.assert_called()
