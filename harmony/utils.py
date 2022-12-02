import struct

from harmony.constants import ByteOrder


def float_to_bytes(value: float, byte_order: ByteOrder) -> bytes:
    """Convert a float into bytes

    Args:
        value (float): float to be converted

    Returns:
        bytes: float as an IEEE 754 binary representation
    """
    byte_order_dictionary = {
        ByteOrder.LITTLE: "<",
        ByteOrder.BIG: ">",
    }

    passed_byte_order = byte_order_dictionary[byte_order]
    packed_float = struct.pack(f"{passed_byte_order}f", value)
    return packed_float
