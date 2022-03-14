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

import re
from llvm_diagnostics import messages, utils

DIAGNOSTICS_HEADER = re.compile(
    r"[a-zA-Z\.\_\/\0-9]+:[0-9]+:[0-9]+:\ (?:error|warning|note): .*"
)


def diagnostics_messages_from_file(file_path: str):
    with open(file_path, "r", encoding="UTF-8") as file_obj:
        for line in file_obj:
            _stripped = utils.strip_ansi_escape_chars(line)
            _element = re.search(DIAGNOSTICS_HEADER, _stripped)
            if _element:
                _element = _element.group().strip(" ")
                _file_path, _line_number, _column_number, _level, _message = _element.split(
                    ":", 4
                )

                yield messages.DiagnosticsMessage(
                    file_path=_file_path,
                    line_number=int(_line_number),
                    column_number=int(_column_number),
                    message=_message.rstrip("\n").strip(" "),
                    level=messages.DiagnosticsLevel[_level.strip(" ").upper()],
                )
