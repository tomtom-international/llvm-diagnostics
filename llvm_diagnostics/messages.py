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

"""Diagnostic Messages"""

from dataclasses import dataclass
import json
from sys import stderr
from typing import Optional

from llvm_diagnostics.utils import DiagnosticsLevel
from llvm_diagnostics.formatters import LlvmFormatter, DiagnosticsFormatter


@dataclass
class DiagnosticsRange:
    """Diagnostics Range"""

    start: int = 1
    range: Optional[int] = None


@dataclass
class DiagnosticsMessage:
    """Diagnostics Message"""

    file_path: str
    message: str
    column_number: DiagnosticsRange = DiagnosticsRange()
    expectations: Optional[str] = None
    line: Optional[str] = None
    line_number: DiagnosticsRange = DiagnosticsRange()
    formatter: DiagnosticsFormatter = LlvmFormatter()
    level: DiagnosticsLevel = DiagnosticsLevel.ERROR

    def report(self):
        """Formats the Diagnostics message and sends it to `stderr`"""
        print(self, file=stderr)

    def __str__(self):
        """Formats the Diagnostics message"""
        return self.formatter.format(message=self)

    def to_json(self):
        """Converts the Diagnostics Message to simply JSON format"""
        return json.dumps(
            {
                "filepath": self.file_path,
                "line": self.line_number.start,
                "column": self.column_number.start,
                "level": DiagnosticsLevel(self.level).name.lower(),
                "message": self.message,
            }
        )
