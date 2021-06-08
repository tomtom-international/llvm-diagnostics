================
llvm-diagnostics
================
|version| |license| |coverage| |qualitygate| 

Python module for creating diagnostics using the LLVM diagnostics specification

.. |coverage| image:: https://sonarcloud.io/api/project_badges/measure?project=KevinDeJong-TomTom_llvm_diagnostics&metric=coverage
.. |qualitygate| image:: https://sonarcloud.io/api/project_badges/measure?project=KevinDeJong-TomTom_llvm_diagnostics&metric=alert_status
.. |version| image:: https://badge.fury.io/py/llvm-diagnostics.svg
   :target: https://badge.fury.io/py/llvm-diagnostics
.. |license| image:: https://img.shields.io/pypi/l/llvm-diagnostics.svg
   :target: https://pypi.python.org/pypi/llvm-diagnostics


Installation
------------
.. code-block:: console

   $ pip install llvm-diagnostics

Example
-------

.. code-block:: python

    from llvm_diagnostics import messages

    message = messages.DiagnosticsMessage(
        file_path='fake_file.py',
        line_number=10,
        column_number=15,
        level=messages.DiagnosticsLevel.WARNING,
        message='Value exceeds maximum, automatically capped to 100',
        hint=messages.DiagnosticsHint('mPercentage = 105', mismatch='105', expectation='100')
    ).report()
