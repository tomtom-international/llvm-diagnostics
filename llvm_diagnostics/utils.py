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

from enum import Enum
import re

_ANSI_ESCAPE = re.compile(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")


class TextFormat(Enum):
    BOLD = 1

    RED = 31
    BLUE = 34
    LIGHT_GREEN = 92
    CYAN = 94


def format_string(string: str, color: TextFormat):
    return f"\033[{color.value}m{string}\033[0m"


def strip_ansi_escape_chars(string: str):
    return _ANSI_ESCAPE.sub("", string)
