DataQuality-Manager

Desktop-Anwendung in Python mit PyQt6 und SQLite zur Verwaltung, Validierung, Vorschau und Export/Import von Mitarbeiterdaten inklusive CSV-, und JSON-Report-Unterstützung[cite: 2]. Funktionen

Mitarbeiterverwaltung (SQLite): Anlegen, Bearbeiten, Löschen, Suchen und Filtern von Mitarbeiterdatensätzen (employees) über EmployeeRepository und DatabaseConnection.
Datenqualitätsprüfung (DataValidator): Prüfung von Pflichtfeldern (first_name, last_name, email), E-Mail-Format, optionaler Telefonnummer, Datumsformat (YYYY-MM-DD für birth_date), Datumslogik sowie Duplikat-Erkennung (ERROR und WARNING).
CSV-Import/Export: Einlesen mit Vorschau und Live-Validierung über CsvImporter sowie Export in CSV (CsvExporter).
Qualitätsberichte & Statistiken: Erstellung von JSON-Berichten (ReportGenerator) und Kennzahlenberechnung (StatisticsService) sowie Anzeige im Dashboard und in den UI-Views.
Nachverfolgung: Speicherung von Validierungsergebnissen (validation_results) und Import-Historie (import_history) in SQLite.

Projektstruktur

main.py – Einstiegspunkt der Anwendung, Logging-Konfiguration und Initialisierung[cite: 1].
database/ – SQLite-Verbindung (connection.py), Schema (schema.sql) und Repository (employee_repository.py)[cite: 1].
models/ – Datenmodelle (employee.py, validation_result.py)[cite: 1].
services/ – Geschäftslogik für Validierung, CSV, Statistik und JSON-Reports[cite: 1].
ui/ – PyQt6-Oberfläche (main_window.py, dashboard.py, employee_view.py, import_view.py, validation_view.py)[cite: 1].
tests/ – Unit- und Integrationstests (test_database.py, test_importer.py, test_validator.py)[cite: 1].

Installation & Start

Abhängigkeiten installieren:

pip install -r requirements.txt
