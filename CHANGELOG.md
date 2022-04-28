<!--
Copyright (C) 2022 TomTom NV. All rights reserved.

This software is the proprietary copyright of TomTom NV and its subsidiaries and may be
used for internal evaluation purposes or commercial use strictly subject to separate
license agreement between you and TomTom NV. If you are the licensee, you are only permitted
to use this software in accordance with the terms of your license agreement. If you are
not the licensee, you are not authorized to use this software in any manner and should
immediately return or destroy it.
-->

# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.1.0]
### Added
- Add support for Python versions `>=3.7`

## [2.0.1] - 2022-04-15
### Fixed
- Diagnostics messages without a line are now properly reported with the GitHub formatter

## [2.0.0] - 2022-03-15
### Removed
- Removed the `to_json()` method as it was only used for validation

### Added
- New classes representing the message type (`DiagnosticsError`, `DiagnosticsWarning`, `DiagnosticsInfo`)

### Changed
- Allow creation of a diagnostics message without `file_path`

## [1.0.0] - 2022-03-15
### Removed
- Both `line_number` and `column_number` properties have been reworked
- Removed `DiagnosticsHint` property from `DiagnosticsMessage`
- Removed several type checks in favor of relying on type hinting

### Added
- GitHub-formatter for reporting LLVM Diagnostics messages in GitHub actions

### Deprecated
- Migrate from Python 3.7 to Python 3.9

### Fixed
- Resolved many issues when trying to specify hints


