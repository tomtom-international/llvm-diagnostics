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
import json
from sys import stderr
from typing import Optional

from llvm_diagnostics import utils


class DiagnosticsLevel(Enum):
    ERROR = utils.format_string("error", utils.TextFormat.RED)
    WARNING = utils.format_string("warning", utils.TextFormat.CYAN)
    NOTE = utils.format_string("note", utils.TextFormat.BLUE)


class DiagnosticsHint:
    def __init__(
        self,
        line: str,
        mismatch: Optional[str] = None,
        expectation: Optional[str] = None,
    ):
        self.line = line.rstrip("\n") if line is not None else None
        self.mismatch = mismatch.rstrip("\n") if mismatch is not None else None
        self.expectation = expectation.rstrip("\n") if expectation is not None else None
        self.column_number = 0

    @property
    def column_number(self):
        return self.__column_number

    @column_number.setter
    def column_number(self, column_number: int):
        if not isinstance(column_number, int):
            raise TypeError("Incorrect type for property: column number")

        self.__column_number = column_number

    def __str__(self):
        _comp = None

        if self.mismatch is not None:
            _comp = self.line[
                self.column_number - 1: self.column_number + len(self.mismatch)
            ]

            if _comp != self.mismatch:
                raise Exception(f"Expected '{self.mismatch}', found '{_comp}'")

        if self.expectation:
            _expectation = "\n" + (" " * (self.column_number - 1)) + self.expectation

        return (
            self.line
            + "\n"
            + (" " * (self.column_number - 1))
            + utils.format_string("^", utils.TextFormat.LIGHT_GREEN)
            + (
                utils.format_string("~" * (len(self.mismatch) - 1), utils.TextFormat.LIGHT_GREEN)
                if _comp
                else ""
            )
            + (_expectation if self.expectation else "")
        )


class DiagnosticsMessage:
    def __init__(
        self,
        file_path: str,
        line_number: int,
        column_number: int,
        message: str,
        level: DiagnosticsLevel = DiagnosticsLevel.ERROR,
        hint: Optional[DiagnosticsHint] = None,
    ):
        self.hint = hint
        if hint is not None:
            hint.column_number = column_number

        self.file_path = file_path
        self.line_number = line_number
        self.column_number = column_number
        self.level = level
        self.message = message

    @property
    def file_path(self):
        return self.__file_path

    @file_path.setter
    def file_path(self, file_path: str):
        self.__file_path = file_path

    @property
    def line_number(self):
        return self.__line_number

    @line_number.setter
    def line_number(self, line_number: int):
        if not isinstance(line_number, int):
            raise TypeError("Incorrect type for property: line number")

        self.__line_number = line_number

    @property
    def column_number(self):
        return self.__column_number

    @column_number.setter
    def column_number(self, column_number: int):
        if not isinstance(column_number, int):
            raise TypeError("Incorrect type for property: column number")

        self.__column_number = column_number

        if hasattr(self, "hint") and self.hint is not None:
            self.__hint.column_number = column_number

    @property
    def level(self):
        return self.__level

    @level.setter
    def level(self, level: DiagnosticsLevel):
        if not isinstance(level, DiagnosticsLevel):
            raise TypeError("Incorrect type for property: level")

        self.__level = level

    @property
    def message(self):
        return self.__message

    @message.setter
    def message(self, message: str):
        if not isinstance(message, str):
            raise TypeError("Incorrect type for property: message")

        self.__message = message.rstrip("\n")

    @property
    def hint(self):
        return self.__hint

    @hint.setter
    def hint(self, hint: DiagnosticsHint):
        if hint is None:
            self.__hint = hint
            return

        if not isinstance(hint, DiagnosticsHint):
            raise TypeError("Incorrect type for property: hint")

        if hasattr(self, "column_number"):
            hint.column_number = self.column_number

        self.__hint = hint

    def report(self):
        print(self, file=stderr)

    def __str__(self):
        _string = utils.format_string(
            f"{self.file_path}:{self.line_number}:{self.column_number}: {self.level.value}: {self.message}",
            utils.TextFormat.BOLD,
        )

        if self.hint:
            _string += f"\n{self.hint}"

        return _string

    def to_json(self):
        return json.dumps(
            {
                "filepath": self.file_path,
                "line": self.line_number,
                "column": self.column_number,
                "level": utils.strip_ansi_escape_chars(self.level.value),
                "message": self.message,
            }
        )
