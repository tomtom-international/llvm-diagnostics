# Copyright (c) 2022 - 2022 TomTom N.V.
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

"""Diagnostic Message Formatters"""

import os
from typing import Any, Protocol

from llvm_diagnostics import utils
from llvm_diagnostics.utils import DiagnosticsLevel


class DiagnosticsFormatter(Protocol):
    """Protocol Formatter class"""

    def format(self, message: Any) -> str:
        """Protocol method"""
        ...


class LlvmFormatter(DiagnosticsFormatter):
    """LLVM Diagnostics Formatter"""

    LEVEL_FORMAT = {
        DiagnosticsLevel.ERROR: utils.format_string("error", utils.TextFormat.RED),
        DiagnosticsLevel.WARNING: utils.format_string("warning", utils.TextFormat.RED),
        DiagnosticsLevel.NOTE: utils.format_string("note", utils.TextFormat.RED),
    }

    def format(self, message: Any) -> str:
        """Formats the Diagnostics message into a LLVM Diagnostics compatible format"""
        _message = utils.format_string(
            f"{message.file_path}:{message.line_number.start}:{message.column_number.start}: {self.LEVEL_FORMAT[message.level]}: {message.message}",
            utils.TextFormat.BOLD,
        )

        if not message.line:
            return _message

        _indicator = (
            message.line.rstrip(os.linesep)
            + os.linesep
            + " " * (message.column_number.start - 1)
            + utils.format_string("^", utils.TextFormat.LIGHT_GREEN)
        )

        if message.column_number.range:
            _indicator += utils.format_string(
                "~" * (message.column_number.range - 1), utils.TextFormat.LIGHT_GREEN
            )

        if message.expectations:
            _indicator += (
                os.linesep
                + " " * (message.column_number.start - 1)
                + message.expectations
            )

        return _message + os.linesep + _indicator


class GitHubFormatter(DiagnosticsFormatter):
    """GitHub Formatter"""

    LEVEL_FORMAT = {
        DiagnosticsLevel.ERROR: "error",
        DiagnosticsLevel.WARNING: "warning",
        DiagnosticsLevel.NOTE: "notice",
    }

    def format(self, message: Any) -> str:
        """Formats the Diagnostics message into a GitHub compatible Workflow command"""

        _message = f"::{self.LEVEL_FORMAT[message.level]} file={message.file_path}"

        if not message.line:
            return _message

        _message += f",line={message.line_number.start}"
        if message.line_number.range:
            _message += (
                f",endLine={message.line_number.start + message.line_number.range}"
            )

        _message += f",col={message.column_number.start}"
        if message.column_number.range:
            _message += f",endColumn={message.column_number.start + message.column_number.range}"

        _message += f"::{message.message}"

        return _message