# DataQuality Manager
### CSV-Datenmanagement und Qualitätsprüfung mit Python

DataQuality Manager ist eine Desktop-Anwendung zur Verwaltung und Überprüfung von Mitarbeiterdaten. CSV-Dateien können eingelesen, geprüft und als Vorschau angezeigt werden. Die Anwendung ist darauf ausgelegt, fehlerhafte, unvollständige oder doppelte Datensätze zu erkennen, Mitarbeiterdaten zu verwalten und Ergebnisse zu exportieren.

**Projektstatus:** Diese README beschreibt den geplanten Funktionsumfang des Teamprojekts. Bitte aktualisiert den Feature-Status und die Installationshinweise, sobald die Implementierung abgeschlossen ist und die Projektdateien sowie Schnittstellen festgelegt wurden.

## Inhaltsverzeichnis

- [Projektziel](#projektziel)
- [Funktionen](#funktionen)
- [Technologien](#technologien)
- [Voraussetzungen](#voraussetzungen)
- [Installation](#installation)
- [Anwendung starten](#anwendung-starten)
- [CSV-Dateiformat](#csv-dateiformat)
- [Projektstruktur](#projektstruktur)
- [Datenqualitätsprüfung](#datenqualitätsprüfung)
- [Benutzeroberfläche](#benutzeroberfläche)
- [Mögliche Erweiterungen](#mögliche-erweiterungen)

## Projektziel

Unternehmen erhalten Mitarbeiterdaten aus verschiedenen Abteilungen in CSV-Dateien. Diese Dateien können fehlende Angaben, ungültige Werte, Duplikate oder uneinheitliche Daten enthalten.

DataQuality Manager soll eine Desktop-Anwendung zum Importieren, Verwalten, Prüfen und Exportieren dieser Daten bereitstellen.

Das Ziel ist eine übersichtliche und zuverlässige Datenverwaltung mit verständlichen Fehlermeldungen und Datenqualitätsberichten.

## Funktionen

Der geplante Mindestumfang umfasst:

- **CSV-Import:** CSV-Dateien auswählen, einlesen und auf erforderliche Spalten prüfen.
- **Import-Vorschau:** Eingelesene Datensätze vor der weiteren Verarbeitung in einer Tabelle anzeigen.
- **Mitarbeiterverwaltung:** Mitarbeiterdaten anzeigen, hinzufügen, bearbeiten und löschen.
- **Datenqualitätsprüfung:** Fehlende Pflichtwerte, ungültige E-Mail-Adressen, doppelte Datensätze, ungültige Datumsangaben und fehlerhafte Telefonnummern erkennen.
- **Datenbank:** Mitarbeiterdaten, Prüfergebnisse und Importhistorie in SQLite speichern.
- **Suche und Filter:** Datensätze nach Name oder E-Mail durchsuchen sowie nach Abteilung oder Prüfstatus filtern.
- **Export:** Daten als CSV sowie Qualitätsberichte und Fehlerberichte als JSON exportieren.
- **Fehlerbehandlung:** Verständliche Hinweise bei fehlenden Dateien, ungültigen CSV-Dateien oder Datenbankfehlern anzeigen.

## Technologien

- Python 3
- PyQt6 – Grafische Benutzeroberfläche
- CSV – Import und Export von CSV-Dateien
- SQLite – Persistente Datenspeicherung
- JSON – Datenqualitätsberichte
- Git – Versionsverwaltung und Zusammenarbeit

## Voraussetzungen

- Python 3.10 oder eine kompatible, vom Team festgelegte Version
- pip
- Git

## Installation

### 1. Repository klonen
```bash
git clone <REPOSITORY-URL>
```

### 2. In das Projektverzeichnis wechseln
```bash
cd DataQualityManager
```

### 3. Abhängigkeiten installieren
```bash
pip install PyQt6
```
Falls eine `requirements.txt`-Datei vorhanden ist, können alle Abhängigkeiten mit folgendem Befehl installiert werden:
```bash
pip install -r requirements.txt
```

## Anwendung starten

Starte die Anwendung mit:
```bash
python3 main.py
```

**ODER** über eine virtuelle Umgebung (`venv`):

1. Virtuelle Umgebung erstellen:
   ```bash
   python3 -m venv venv
   ```
2. Umgebung aktivieren:
   - **Windows:** `venv\Scripts\activate`
   - **Linux/macOS:** `source venv/bin/activate`
3. Abhängigkeiten installieren:
   ```bash
   pip install -r requirements.txt
   ```
4. Anwendung starten:
   ```bash
   python3 main.py
   ```

## CSV-Dateiformat

Die CSV-Datei sollte folgende Spalten enthalten:

```csv
first_name,last_name,email,phone,department
Max,Mustermann,max@test.de,0171234567,IT
Anna,Schmidt,anna@test.de,0171234568,HR
Peter,,peter@test.de,0171234569,IT
Max,Mustermann,max@test.de,0171234567,IT
Lisa,Meyer,invalid-email,0171234560,Sales
```

Beim Import sollen fehlende erforderliche Spalten erkannt und dem Benutzer gemeldet werden.

## Projektstruktur

Das Projekt soll einer modularen Struktur folgen. Die endgültige Struktur kann sich während der Entwicklung noch ändern.

```text
DataQualityManager/
│
├── main.py
├── requirements.txt
│
├── database/
│
├── models/
│
├── services/
│
├── ui/
│
├── tests/
│
├── data/
│
└── reports/
```

## Datenqualitätsprüfung

Die Anwendung ist darauf ausgelegt, häufige Probleme bei der Datenqualität zu erkennen, darunter:

- Fehlende Pflichtwerte
- Ungültige E-Mail-Adressen
- Doppelte Mitarbeiterdatensätze
- Ungültige Datumsangaben
- Fehlerhafte Telefonnummern

Die Entscheidung des Teams über den Umgang mit fehlerhaften Datensätzen oder Warnungen (z. B. speichern, ablehnen oder den Import dennoch zulassen) wird während der Entwicklung festgelegt.

## Benutzeroberfläche

Die Anwendung wird eine grafische Benutzeroberfläche zum Importieren, Anzeigen, Verwalten und Prüfen von Mitarbeiterdaten bereitstellen.

Screenshots der Anwendung können hier hinzugefügt werden, sobald die Oberfläche implementiert wurde.

## Mögliche Erweiterungen

Die folgenden Funktionen sind optionale Erweiterungen und sollen die Umsetzung der Kernfunktionen nicht blockieren:

- MySQL als alternative Datenbank
- Benutzeranmeldung und Passwortverwaltung
- Dashboard-Diagramme und Statistiken
- Konfigurierbare Validierungsregeln
- Logging (Protokollierung)
- Zusätzliche CSV-Importprofile
