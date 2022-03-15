# Copyright (c) 2021 - 2021 TomTom N.V.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Utilities"""

from enum import Enum, auto
import re

_ANSI_ESCAPE = re.compile(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")


class TextFormat(Enum):
    """ANSI Code text formatting"""

    BOLD = 1

    RED = 31
    BLUE = 34
    LIGHT_GREEN = 92
    CYAN = 94


def format_string(string: str, color: TextFormat):
    """Applies ANSI code formatting to string"""
    return f"\033[{color.value}m{string}\033[0m"


def strip_ansi_escape_chars(string: str):
    """Removes all ANSI code characters from string"""
    return _ANSI_ESCAPE.sub("", string)


class DiagnosticsLevel(Enum):
    """Diagnostics Level"""

    ERROR = auto()
    WARNING = auto()
    NOTE = auto()
