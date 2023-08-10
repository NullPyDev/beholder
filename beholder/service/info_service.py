from abc import ABC, abstractmethod


class InfoService(ABC):
    """Common interface shared among any class that provides system information and statistics for a certain aspect of
    the system.
    """

    @abstractmethod
    def get_info(self) -> dict[str, any]:
        """Retrieves the desired information and statistics for a certain aspect of the system.

        :return: Information and statistics gathered by the info service.
        """
