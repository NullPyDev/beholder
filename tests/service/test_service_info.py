import os
import unittest
from unittest.mock import patch, MagicMock

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
        os.environ["BEHOLDER_SERVICES_WATCHLIST"] = "crond, cupsd"
        self.service: ServiceInfoService = ServiceInfoService()
        self.result: dict[str, any] = self.service.get_info()
        del os.environ["BEHOLDER_SERVICES_WATCHLIST"]

    def test_resultIsNotEmpty(self):
        assert_that(self.result.items()).is_length(2)

    def test_listedServicesAreInTheResult(self):
        assert_that(self.result).contains_key("crond", "cupsd")
        assert_that(self.result["crond"]).is_type_of(bool)
        assert_that(self.result["cupsd"]).is_type_of(bool)


class TestWithErrorToProbeService(unittest.TestCase):

    def setUp(self) -> None:
        os.environ["BEHOLDER_SERVICES_WATCHLIST"] = "crond"
        self.service: ServiceInfoService = ServiceInfoService()

    @patch("subprocess.Popen", autospec=True)
    def test_failSilentlyWhenExceptionOccurs(self, mock_popen):
        mock_process = MagicMock()
        mock_process.communicate.side_effect = FileNotFoundError("Fake Error")
        mock_popen.return_value = mock_process

        result: dict[str, any] = self.service.get_info()

        assert_that(result["crond"]).is_false()
        mock_process.communicate.assert_called_once()

    @patch("subprocess.Popen", autospec=True)
    def test_failSilentlyWhenReturningError(self, mock_popen):
        mock_process = MagicMock()
        mock_process.communicate.return_value = (None, {"error": "Fake Error"})
        mock_popen.return_value = mock_process

        result: dict[str, any] = self.service.get_info()

        assert_that(result["crond"]).is_false()
        mock_process.communicate.assert_called_once()
