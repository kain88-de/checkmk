#!/usr/bin/env python3
# Copyright (C) 2019 tribe29 GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.
import ast


class FakeStatusSocket:
    def __init__(self, query: bytes) -> None:
        self._query = query
        self._sent = False
        self._response = b""

    def recv(self, size: int) -> bytes:
        if self._sent:
            return b""

        self._sent = True
        return self._query

    def sendall(self, data: bytes) -> None:
        self._response += data

    def close(self) -> None:
        pass

    def get_response(self) -> list:
        response = ast.literal_eval(self._response.decode("utf-8"))
        # assert isinstance(response, list)
        return response
