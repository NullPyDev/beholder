import locale
import platform
import unittest
from datetime import datetime

import psutil
from assertpy import assert_that
from tzlocal.unix import get_localzone

from beholder import BEHOLDER_VERSION
from beholder.service.system_info_service import SystemInfoService


class TestSystemInfoService(unittest.TestCase):

    def setUp(self) -> None:
        self.service: SystemInfoService = SystemInfoService()
        self.result: dict[str, any] = self.service.get_info()

    def test_systemIsAvailable(self):
        assert_that(self.result).contains("system")
        assert_that(self.result["system"]).is_equal_to(platform.uname().system)

    def test_hostNameIsAvailable(self):
        assert_that(self.result).contains("host_name")
        assert_that(self.result["host_name"]).is_equal_to(platform.uname().node)

    def test_releaseIsAvailable(self):
        assert_that(self.result).contains("release")
        assert_that(self.result["release"]).is_equal_to(platform.uname().release)

    def test_architectureIsAvailable(self):
        assert_that(self.result).contains("architecture")
        assert_that(self.result["architecture"]).is_equal_to(platform.uname().machine)

    def test_beholderVersionIsAvailable(self):
        assert_that(self.result).contains("beholder_version")
        assert_that(self.result["beholder_version"]).is_equal_to(BEHOLDER_VERSION)

    def test_bootTimeIsAvailable(self):
        assert_that(self.result).contains("boot_time")
        assert_that(self.result["boot_time"]).is_equal_to(
            datetime.fromtimestamp(psutil.boot_time())
        )

    def test_localeIsAvailable(self):
        assert_that(self.result).contains("locale")
        assert_that(self.result["locale"]).is_equal_to(locale.getlocale()[0])

    def test_encodingIsAvailable(self):
        assert_that(self.result).contains("encoding")
        assert_that(self.result["encoding"]).is_equal_to(locale.getlocale()[1])

    def test_timeZoneIsAvailable(self):
        assert_that(self.result).contains("time_zone")
        assert_that(self.result["time_zone"]).is_equal_to(get_localzone().key)

    def test_currentTimeIsAvailable(self):
        assert_that(self.result).contains("current_time")
        assert_that(self.result["current_time"]).is_not_empty()

    def test_upTimeIsAvailable(self):
        assert_that(self.result).contains("up_time")
        assert_that(self.result["up_time"]).matches("[0-9]* day\\(s\\)\\, [0-9]* hour\\(s\\)* and [0-9]* minute\\(s\\)")
