# Copyright (c) 2021 - 2022 TomTom N.V.
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
# limitations under the License.import re

import re

from llvm_diagnostics import utils
import llvm_diagnostics


ANSI_ESCAPE = re.compile(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")


def test_warning_message_complete():
    _expectation = """\
fake_file.py:10:15: warning: Value exceeds maximum, automatically capped to 100\n\
mPercentage = 105\n\
              ^~~\n\
              100\
"""
    _output = str(llvm_diagnostics.Error(
        file_path="fake_file.py",
        line_number=llvm_diagnostics.Range(start=10),
        column_number=llvm_diagnostics.Range(start=15, range=3),
        line="mPercentage = 105",
        expectations="100",
        level=llvm_diagnostics.Level.WARNING,
        message="Value exceeds maximum, automatically capped to 100",
    ))

    assert utils.strip_ansi_escape_chars(_output) == _expectation


def test_error_message_no_expectation():
    _expectation = """\
fake_file.py:10:15: error: Incorrect type assigned to mPercentage\n\
mPercentage = \"105\"\n\
              ^~~~~\
"""
    _output = str(llvm_diagnostics.Error(
        file_path="fake_file.py",
        line_number=llvm_diagnostics.Range(start=10),
        column_number=llvm_diagnostics.Range(start=15, range=5),
        line="mPercentage = \"105\"",
        message="Incorrect type assigned to mPercentage",
    ))

    assert utils.strip_ansi_escape_chars(_output) == _expectation


def test_note_message_no_mismatch_and_exceptation():
    _expectation = """\
fake_file.py:10:1: note: mPercentage is deprecated and will be removed in 2030\n\
mPercentage = 105\n\
^\
"""
    _output = str(llvm_diagnostics.Info(
        file_path="fake_file.py",
        line_number=llvm_diagnostics.Range(start=10),
        column_number=llvm_diagnostics.Range(start=1),
        line="mPercentage = 105",
        message="mPercentage is deprecated and will be removed in 2030",
    ))

    assert utils.strip_ansi_escape_chars(_output) == _expectation


def test_note_message_minimal():
    _expectation = "fake_file.py:1:1: note: Missing copyright information"
    _output = str(llvm_diagnostics.Info(
        file_path="fake_file.py",
        message="Missing copyright information",
    ))

    assert utils.strip_ansi_escape_chars(_output) == _expectation
