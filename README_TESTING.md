DataQuality Testing Dashboard
Project Description:

The Testing Dashboard is a standalone desktop application for quality assurance of the DataQuality Manager project.

The application was developed using Python and PyQt6.

Area of Responsibility:

Task 8: Integration and Testing

My responsibilities include:

Development of a Test Runner
Evaluation of test results
Automated testing with pytest
Integration testing
Development of a graphical Testing Dashboard
Creation of JSON test reports
Technologies
Python
PyQt6
pytest
unittest
SQLite
JSON
Git and GitHub
Installation

Activate the virtual environment:
source venv/bin/activate

Install dependencies:
python -m pip install -r requirements.txt
python -m pip install pytest PyQt6

Start the Testing Dashboard
QT_QPA_PLATFORM=xcb python testing_main.py

Automated Tests
Run all tests:
python -m pytest -v

Run integration tests:
python -m pytest -v tests/test_integration.py

Dashboard Features
Run All Tests
Run Database Tests
Run Import Tests
Run Validation Tests
Run Integration Tests
Show Results
Show Failed Tests
Export JSON Report

Integration Test

The integration test checks the following workflow:

CSV Import -> Data Validation -> SQLite -> CSV Export

Test Results

Last documented test run:

Total Tests: 10
Passed: 10
Failed: 0
Skipped: 0
Status: PASSED
JSON Test Report

The report is saved at:
reports/test_report.json

Screenshots

Testing Dashboard
docs/testing_dashboard1.png

Integration Testing
docs/integration_test1.png
docs/integration_test2.png