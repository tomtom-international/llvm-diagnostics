import re

from llvm_diagnostics import utils
from llvm_diagnostics import DiagnosticsError, DiagnosticsInfo, DiagnosticsRange, DiagnosticsLevel


ANSI_ESCAPE = re.compile(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")


def test_warning_message_complete():
    _expectation = """\
fake_file.py:10:15: warning: Value exceeds maximum, automatically capped to 100\n\
mPercentage = 105\n\
              ^~~\n\
              100\
"""
    _output = str(DiagnosticsError(
        file_path="fake_file.py",
        line_number=DiagnosticsRange(start=10),
        column_number=DiagnosticsRange(start=15, range=3),
        line="mPercentage = 105",
        expectations="100",
        level=DiagnosticsLevel.WARNING,
        message="Value exceeds maximum, automatically capped to 100",
    ))

    assert utils.strip_ansi_escape_chars(_output) == _expectation


def test_error_message_no_expectation():
    _expectation = """\
fake_file.py:10:15: error: Incorrect type assigned to mPercentage\n\
mPercentage = \"105\"\n\
              ^~~~~\
"""
    _output = str(DiagnosticsError(
        file_path="fake_file.py",
        line_number=DiagnosticsRange(start=10),
        column_number=DiagnosticsRange(start=15, range=5),
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
    _output = str(DiagnosticsInfo(
        file_path="fake_file.py",
        line_number=DiagnosticsRange(start=10),
        column_number=DiagnosticsRange(start=1),
        line="mPercentage = 105",
        message="mPercentage is deprecated and will be removed in 2030",
    ))

    assert utils.strip_ansi_escape_chars(_output) == _expectation


def test_note_message_minimal():
    _expectation = "fake_file.py:1:1: note: Missing copyright information"
    _output = str(DiagnosticsInfo(
        file_path="fake_file.py",
        message="Missing copyright information",
    ))

    assert utils.strip_ansi_escape_chars(_output) == _expectation
