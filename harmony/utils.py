import struct


def float_to_bytes(value: float) -> bytes:
    """Convert a float into bytes

    Args:
        value (float): float to be converted

    Returns:
        bytes: float as an IEEE 754 binary representation
    """
    packed_float = struct.pack(">f", value)
    return packed_float
