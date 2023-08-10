import datetime
import locale
import platform

import psutil

from beholder import BEHOLDER_VERSION
from tzlocal import get_localzone

from ..service.info_service import InfoService


class SystemInfoService(InfoService):
    """Info service implementation specialized to retrieve the basic details about the node."""

    # Details about kernel, os and its versions.
    __uname: platform.uname_result = None

    # Cache of immutable system details.
    __info: dict[str, any] = None

    def __init__(self):
        """Default class constructor. Initialized the "uname" attribute."""
        self.__uname = platform.uname()

    def get_info(self) -> dict[str, any]:
        """
        Retrieve, format and return the basic system details, The returned dictionary contains the following entries:

        * system: Operation system.
        * host_name: Name of the host.
        * release: Kernel version.
        * architecture: Node architecture (e.g.: x86, x86_64).
        * beholder_version: Version of Beholder service.
        * boot_time: Timestamp of when the system started.
        * locale: Node's configured locale.
        * encoding: Node's configured encoding.
        * time_zone: Node's configured timezone.
        * current_time: Node's current date and time.
        * up_time: Time passed since the node started.

        :return: A dictionary containing the aforementioned entries.
        """
        if not self.__info:
            self.__info = {
                "system": self.__uname.system,
                "host_name": self.__uname.node,
                "release": self.__uname.release,
                "architecture": self.__uname.machine,
                "beholder_version": BEHOLDER_VERSION,
                "boot_time": datetime.datetime.fromtimestamp(psutil.boot_time()),
            }

        self.__info["locale"] = locale.getlocale()[0]
        self.__info["encoding"] = locale.getlocale()[1]
        self.__info["time_zone"] = get_localzone().key
        self.__info["current_time"] = datetime.datetime.now().strftime("%d/%m/%Y - %H:%M:%S")
        self.__info["up_time"] = self.get_uptime()
        return self.__info

    def get_uptime(self) -> str:
        """Format the up-time value, showing by default, days, hours and minutes since the host started.

        :return: Up-time formatted as aforementioned.
        """
        now: datetime.datetime = datetime.datetime.utcnow()
        delta: datetime.timedelta = now - self.__info["boot_time"]

        days: int = delta.days
        hours, rem = divmod(delta.seconds, 3_600)
        minutes, seconds = divmod(rem, 60)

        return f"{days} day(s), {hours} hour(s) and {minutes} minute(s)"
