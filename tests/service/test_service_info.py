import os
import unittest

from assertpy import assert_that

from beholder.service.service_info_service import ServiceInfoService


class TestWithNoServiceOnWatchList(unittest.TestCase):
    def setUp(self) -> None:
        os.environ["BEHOLDER_SERVICES_WATCHLIST"] = ""
        self.service: ServiceInfoService = ServiceInfoService()
        self.result: dict[str, any] = self.service.get_info()

    def test_resultIsEmpty(self):
        assert_that(self.result).is_empty()


class TestWithServiceOnWatchlist(unittest.TestCase):
    def setUp(self) -> None:
        os.environ["BEHOLDER_SERVICES_WATCHLIST"] = "crond,cupsd,fake"
        self.service: ServiceInfoService = ServiceInfoService()
        self.result: dict[str, any] = self.service.get_info()
        del os.environ["BEHOLDER_SERVICES_WATCHLIST"]

    def test_resultIsNotEmpty(self):
        assert_that(self.result.items()).is_not_empty()

    def test_listedServicesAreInTheResult(self):
        assert_that(self.result).contains_key("crond", "cupsd", "fake")
        assert_that(self.result["crond"]).is_type_of(bool)
        assert_that(self.result["cupsd"]).is_type_of(bool)
        assert_that(self.result["fake"]).is_type_of(bool)
