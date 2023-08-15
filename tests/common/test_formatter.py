import unittest

from assertpy import assert_that

from beholder.common.formatter import size_formatter, frequency_formatter


class TestSizeFormatter(unittest.TestCase):
    def test_formatBytes(self):
        result: str = size_formatter(124)
        assert_that(result).is_equal_to("124.00 B")

    def test_formatWithThousandSeparator(self):
        result: str = size_formatter(1010)
        assert_that(result).is_equal_to("1,010.00 B")

    def test_formatKiloBytes(self):
        result: str = size_formatter(2_560)
        assert_that(result).is_equal_to("2.50 KB")

    def test_formatMegaBytes(self):
        result: str = size_formatter(1_572_864)
        assert_that(result).is_equal_to("1.50 MB")

    def test_formatGigaBytes(self):
        result: str = size_formatter(1_395_864_371)
        assert_that(result).is_equal_to("1.30 GB")

    def test_formatTeraBytes(self):
        result: str = size_formatter(1_759_218_604_000)
        assert_that(result).is_equal_to("1.60 TB")


class TestFrequencyFormatter(unittest.TestCase):

    def test_formatMegaHertz(self):
        result: str = frequency_formatter(200)
        assert_that(result).is_equal_to("200.00 Mhz")

    def test_formatGigaHertz(self):
        result: str = frequency_formatter(2_300)
        assert_that(result).is_equal_to("2.30 Ghz")
