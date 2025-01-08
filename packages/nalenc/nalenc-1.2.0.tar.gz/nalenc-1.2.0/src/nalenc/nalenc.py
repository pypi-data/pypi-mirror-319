"""
   NAL Encryption. Easy encryption
   Copyright (C) 2025 David Lishchyshen

   This library is free software; you can redistribute it and/or
   modify it under the terms of the GNU Lesser General Public
   License as published by the Free Software Foundation; either
   version 3 of the License, or (at your option) any later version.

   This library is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
   Lesser General Public License for more details.

   You should have received a copy of the GNU Lesser General Public License
   along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

from collections import deque
from typing import Iterable
import numpy as np
from numpy import typing as npt

input_type = str | bytes | Iterable[int] | npt.NDArray[np.uint8]


class NALEnc:
    def __init__(self, passwd: input_type):
        passwd_encoded = self.__encode_value(passwd)
        if len(passwd_encoded) != 512: raise ValueError("passwd len must equal 512 byte")
        self.__passwd = passwd_encoded
        self.__prepare_passwds()

    def encrypt(self, msg: input_type) -> list[int]:
        message = self.__encode_value(msg)
        message = self.__finish_message(message)

        parts = self.__split_message(message)

        for i in range(256):
            parts[:3] = parts[:3] ^ parts[1:4]
            parts = np.array([self.__crypt_part(part, i, idx) for idx, part in enumerate(parts)],np.uint8)  # type: ignore
            parts = np.roll(parts, 1, 0)

        res = np.ravel(parts)

        return res.tolist()

    def decrypt(self, msg: input_type) -> list[int]:
        message = self.__encode_value(msg)

        parts = self.__split_message(message)

        assert parts.ndim == 2

        for i in range(256):
            parts = np.roll(parts, -1, 0)
            parts = np.array([self.__crypt_part(part, i, idx, True) for idx, part in enumerate(parts)], np.uint8) # type: ignore
            for k in range(3):
                parts[2 - k] = parts[2 - k] ^ parts[3 - k]

        res = np.ravel(parts)

        return self.__cut_message(res).tolist() # type: ignore

    def __crypt_part(self, part: npt.NDArray[np.uint8], i: int, part_num: int,
                     decrypt: bool = False) -> npt.NDArray[np.uint8]:
        if len(part) % 512 != 0 or len(part) == 0: raise ValueError("Part length must be equal 526k, k != 0")
        used_prepared_passwd = self.__prepared_passwds[-i-1 if decrypt else i]
        shifts = np.arange(len(part) // 512) + part_num
        passwd = np.concatenate([np.roll(used_prepared_passwd, shift) for shift in shifts])

        part = part ^ passwd
        return part

    def __prepare_passwds(self) -> None:
        idx_array = np.arange(512)
        self.__prepared_passwds = np.empty((256, 512), np.uint8)
        self.__prepared_passwds[0] = self.__passwd
        self.__prepared_passwds[1] = np.where(idx_array != 0,
                                              self.__prepared_passwds[0] ^ self.__prepared_passwds[0, 0],
                                              self.__prepared_passwds[0])
        for i in range(1, 255):
            xor_value = self.__prepared_passwds[i - 1][i]
            self.__prepared_passwds[i + 1] = np.where(idx_array != i, self.__prepared_passwds[i - 1] ^ xor_value,
                                                      self.__prepared_passwds[i - 1])

    def __finish_message(self, msg: npt.NDArray[np.uint8]) -> npt.NDArray[np.uint8]:
        additional_len = 2046 - (len(msg) % 2046) + ((len(msg) // 2048) * 2) % 2046
        if additional_len != 2046 or len(msg) % 2048 == 0:
            res = np.empty(len(msg) + additional_len + 2, np.uint8)
            res[2:len(msg) + 2] = msg
            l1, l2 = additional_len >> 8, additional_len & 0xFF
            current_len = len(msg)
            for i in range(additional_len):
                k = int(self.__passwd[i % len(self.__passwd)])
                res[i + 2 + len(msg)] = np.bitwise_xor(res[(k % current_len) + 2], res[((k + 1) % current_len) + 2])
                current_len += 1
            res[0] = l1
            res[1] = l2
        else:
            res = np.empty(len(msg) + 2, np.uint8)
            res[2:len(msg) + 2] = msg
            res[:2] = np.zeros(2, np.uint8)
        return res

    @staticmethod
    def __split_message(msg: npt.NDArray[np.uint8]) -> npt.NDArray[np.uint8]:
        return np.reshape(msg, (4, len(msg) // 4))

    @staticmethod
    def __encode_value(value: input_type) -> npt.NDArray[np.uint8]:
        try:
            if isinstance(value, str):
                return np.fromiter(value.encode(), np.uint8)
            else:
                return np.fromiter(value, np.uint8)
        except (ValueError, TypeError):
            raise TypeError("Argument must be str | bytes | Iterable[int] | NDArray[uint8]")

    @staticmethod
    def __cut_message(msg: npt.NDArray[np.uint8]) -> npt.NDArray[np.uint8]:
        additional_len = (int(msg[0]) << 8) | int(msg[1])
        return msg[2:len(msg) - int(additional_len)]


__all__ = ["NALEnc"]
