#!/usr/bin/env python3

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

from llvm_diagnostics import parser
import llvm_diagnostics


def _check_expectations_vs_file(file, expectations):
    index = 0
    for item in parser.diagnostics_messages_from_file(file):
        assert isinstance(item, llvm_diagnostics.messages.__Message)
        assert item.file_path == expectations[index].get("filepath")
        assert item.line_number.start == expectations[index].get("line")
        assert item.column_number.start == expectations[index].get("column")
        assert item.message == expectations[index].get("message")
        index += 1


def test_parse_from_logging():
    _check_expectations_vs_file(
        "test/resources/test.out",
        [
            {
                "filepath": "/code/supermarket-buyer-supplier/src/offers/convert_customer_receipt.cpp",
                "line": 295,
                "column": 53,
                "level": "warning",
                "message": "'fruit_section' is deprecated: 2021.Q2 Deprecated Use application::supermarket_app::receipt_engine::receipt::FruitInformation::fruit_section_labels [-Wdeprecated-declarations]",
            },
            {
                "filepath": "/code/.conan/data/supermarket-receipt-engine-interface/18.3.0/application/stable/package/11fb79b907b16b5761824e1660ffa4cace66da21/include/application/supermarket_app/receipt_engine/receipt.hpp",
                "line": 274,
                "column": 5,
                "level": "note",
                "message": "'fruit_section' has been explicitly marked deprecated here",
            },
            {
                "filepath": "/code/.conan/data/framework-customers/0.1.1/application/stable/package/5ab84d6acfe1f23c4fae0ab88f26e3a396351ac9/include/application/supermarket_app/customers.hpp",
                "line": 46,
                "column": 3,
                "level": "note",
                "message": "expanded from macro 'application_supermarket_app_DEPRECATED_MSG'",
            },
            {
                "filepath": "/code/.conan/data/framework-customers/0.1.1/application/stable/package/5ab84d6acfe1f23c4fae0ab88f26e3a396351ac9/include/application/supermarket_app/customers.hpp",
                "line": 40,
                "column": 5,
                "level": "note",
                "message": "expanded from macro '__INTERNAL_DEPRECATED_ATTRIBUTE_MSG'",
            },
            {
                "filepath": "/code/supermarket-buyer-supplier/src/offers/convert_customer_receipt.cpp",
                "line": 383,
                "column": 82,
                "level": "warning",
                "message": "'fruit_section' is deprecated: 2021.Q2 Deprecated Use application::supermarket_app::receipt_engine::receipt::FruitInformation::fruit_section_labels [-Wdeprecated-declarations]",
            },
        ],
    )


def test_parse_from_own_output_file():
    _check_expectations_vs_file(
        "test/resources/own.out",
        [
            {
                "filepath": "fake_file.py",
                "line": 10,
                "column": 15,
                "level": "warning",
                "message": "Value exceeds maximum, automatically capped to 100",
            },
            {
                "filepath": "fake_file.py",
                "line": 10,
                "column": 15,
                "level": "error",
                "message": "Incorrect type assigned to mPercentage",
            },
            {
                "filepath": "fake_file.py",
                "line": 10,
                "column": 1,
                "level": "note",
                "message": "mPercentage is deprecated and will be removed in 2030",
            },
            {
                "filepath": "fake_file.py",
                "line": 0,
                "column": 0,
                "level": "note",
                "message": "Missing copyright information",
            },
        ],
    )
