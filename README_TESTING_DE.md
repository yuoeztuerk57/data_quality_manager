DataQuality Testing Dashboard

Projektbeschreibung:

Das Testing Dashboard ist eine eigenständige Desktop-Anwendung zur Qualitätssicherung des DataQuality Manager-Projekts.

Die Anwendung wurde mit Python und PyQt6 entwickelt.

Verantwortungsbereich:

Aufgabe 8: Integration und Testing

Meine Aufgaben umfassen:

    Entwicklung eines Test Runners
    Auswertung der Testergebnisse
    Automatisierte Tests mit pytest
    Integrationstests
    Entwicklung eines grafischen Testing Dashboards
    Erstellung von JSON-Testberichten

Technologien

    Python
    PyQt6
    pytest
    unittest
    SQLite
    JSON
    Git und GitHub

Installation

Virtuelle Umgebung aktivieren:

source venv/bin/activate

Abhängigkeiten installieren:

python -m pip install -r requirements.txt
python -m pip install pytest PyQt6


Testing Dashboard starten

QT_QPA_PLATFORM=xcb python testing_main.py

Automatisierte Tests
Alle Tests starten:

python -m pytest -v

Integrationstest starten:

python -m pytest -v tests/test_integration.py

Dashboard-Funktionen
Run All Tests
Run Database Tests
Run Import Tests
Run Validation Tests
Run Integration Tests
Show Results
Show Failed Tests
Export JSON Report

Integrationstest

Der Integrationstest überprüft folgenden Workflow:

CSV Import -> Datenvalidierung -> SQLite -> CSV Export

Testergebnisse

Letzter dokumentierter Testlauf:

Total Tests: 10
Passed: 10
Failed: 0
Skipped: 0
Status: PASSED

JSON-Testbericht

Der Bericht wird gespeichert unter:

reports/test_report.json

Screenshots
Testing Dashboard

docs/testing_dashboard1.png
Integration Testing

docs/integration_test1.png
docs/integration_test2.png