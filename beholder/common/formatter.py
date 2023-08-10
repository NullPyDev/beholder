def size_formatter(size, suffix="B") -> str:
    """Format the received value into a proper human-readable data size information.

    :param size: Size to be formatted, expressed in bytes.
    :param suffix: Desired scale suffix. Default: "B".
    :return: Formatted data size, with proper suffix and 2 decimal places.
    """
    factor = 1_024
    for unit in ["", "K", "M", "G", "T"]:
        if size < factor:
            return f"{size:.2f} {unit}{suffix}"
        size /= factor


def frequency_formatter(frequency):
    """Format the received frequency expressed in Mhz into a proper human-readable frequency information.

    :param frequency: Frequency to be formatted, expressed in Mhz.
    :return: Formatted frequency, with proper suffix and 2 decimal places.
    """
    factor = 1_000
    for unit in ["Mhz", "Ghz"]:
        if frequency < factor:
            return f"{frequency:.2f} {unit}"
        frequency /= factor
