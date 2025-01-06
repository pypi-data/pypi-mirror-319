# coding: utf-8
"""
TinyHash
"""

import base64

__author__ = ["FoxMaSk"]
__license__ = "WTFL"
__all__ = ["small_hash"]
__version__ = "0.0.1"

# CRC Stuff


def crc_that(string: str) -> int:
    """
    the PHP's hash(crc32) in Python :P

    implem in python:
       https://chezsoi.org/shaarli/shaare/U7admg
       https://stackoverflow.com/a/50843127/636849
    """
    a = bytearray(string, "utf-8")
    crc = 0xFFFFFFFF
    for x in a:
        crc ^= x << 24
        for k in range(8):
            crc = (crc << 1) ^ 0x04C11DB7 if crc & 0x80000000 else crc << 1
    crc = ~crc
    crc &= 0xFFFFFFFF
    return int.from_bytes(crc.to_bytes(4, "big"), "little")


def small_hash(text: str) -> str:
    """
     Returns the small hash of a string, using RFC 4648 base64url format
    eg. smallHash('20111006_131924') --> yZH23w
    Small hashes:
      - are unique (well, as unique as crc32, at last)
      - are always 6 characters long.
      - only use the following characters: a-z A-Z 0-9 - _ @
      - are NOT cryptographically secure (they CAN be forged)
    In Shaarli (https://sebsauvage.net/wiki/doku.php?id=php:shaarli),
    they are used as a tinyurl-like link to individual entries.
    """
    number = crc_that(text)

    number_bytes = number.to_bytes((number.bit_length() + 7) // 8, byteorder="big")

    encoded = base64.b64encode(number_bytes)
    final_value = encoded.decode().rstrip("=").replace("+", "-").replace("/", "_")
    return final_value
