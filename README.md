

# DataQuality Manager

**Mitarbeiterdaten verwalten. Qualität sichern.**

Eine Desktop-Anwendung zum Importieren, Validieren, Verwalten und Exportieren von Mitarbeiterdaten aus CSV-Dateien – inklusive automatischer Datenqualitätsprüfung, SQLite-Datenhaltung und strukturierten JSON-Qualitätsberichten.

---

## Überblick

Der **DataQuality Manager** unterstützt Unternehmen und Teams dabei, Mitarbeiterdaten vor und nach dem Import zuverlässig zu prüfen und sauber zu halten. Fehlerhafte CSV-Zeilen, fehlende Pflichtspalten, ungültige Formate und Dubletten werden bereits in der Importvorschau erkannt, markiert und können dort direkt korrigiert werden.

---

## Funktionen

* **CSV-Import & Vorschau:** Header-Prüfung auf Pflichtspalten, tolerante Behandlung fehlerhafter Zeilen sowie interaktive Importvorschau mit direkter Bearbeitungsmöglichkeit.
* **Datenvalidierung:** Prüfung auf fehlende Pflichtfelder (`first_name`, `last_name`, `email`), gültige E-Mail- und optionale Telefonnummernformate, logische Geburtsdaten (`YYYY-MM-DD`) sowie Dublettenprüfung (`ERROR` und `WARNING`).
* **Mitarbeiterverwaltung (CRUD):** Tabellarische Anzeige aller gespeicherten Datensätze sowie Anlegen, Bearbeiten und Löschen von Mitarbeitern.
* **Suche, Sortierung & Filterung:** Volltextsuche über relevante Felder, Filterung nach Abteilung und Spaltensortierung in der Tabelle.
* **Persistenz & Nachverfolgung:** Speicherung aller gültigen Mitarbeiterdatensätze, Import-Läufe und Validierungsergebnisse in einer lokalen SQLite-Datenbank.
* **Export & Qualitätsberichte:** Export der Mitarbeiterdaten als CSV-Datei sowie Erstellung strukturierter Qualitätsberichte im JSON-Format.

---

## Tech-Stack

* **Sprache:** Python 3.10+ (objektorientierte Architektur)
* **GUI-Framework:** PyQt6
* **Datenbank:** SQLite (`sqlite3`)
* **Datenformate:** CSV, JSON
* **Plattformen:** GitHub / Codeberg

---

## Projektstruktur

```text
DataQualityManager/
├── main.py                  # Einstiegspunkt der Anwendung & Logging[cite: 1]
├── testing_main.py          # Separater Einstiegspunkt für die Test-GUI
├── requirements.txt         # Projektabhängigkeiten[cite: 1]
├── database/                # SQLite-Verbindung, Schema & Repository (CRUD)[cite: 1]
├── models/                  # Datenmodelle (Employee, ValidationResult, QualityReport)[cite: 1]
├── services/                # CSV-Import/Export, Validierung & Berichtsgenerierung[cite: 1]
├── ui/                      # PyQt6-Hauptfenster, Importvorschau & Dialoge[cite: 1]
├── testing/                 # Unit- und Integrationstests[cite: 1]
└── data/                    # Beispiel-CSV-Dateien & lokale Datenbank
