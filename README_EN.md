# DataQuality Manager
### CSV Data Management and Quality Validation with Python

DataQuality Manager is a desktop application for managing and validating employee data. CSV files can be imported, checked, and displayed in a preview. The application is designed to detect incorrect, incomplete, or duplicate records, manage employee data, and export results.

**Project Status:** This README describes the planned features of the team project. Please update the feature status and installation instructions once implementation is completed and the project files and interfaces have been finalized.

## Table of Contents

- Project Goal
- Features
- Technologies
- Requirements
- Installation
- Running the Application
- CSV File Format
- Project Structure
- Data Quality Validation
- Application User Interface
- Possible Extensions

## Project Goal

Companies receive employee data from different departments in CSV files. These files may contain missing information, invalid values, duplicate records, or inconsistent data.

DataQuality Manager aims to provide a desktop application for importing, managing, validating, and exporting this data.

The goal is to ensure clear and reliable data management, with understandable error messages and data quality reports.

## Features

The planned minimum feature set includes:

- **CSV Import:** Select and read CSV files and check required columns.
- **Import Preview:** Display imported records in a table before further processing.
- **Employee Management:** View, add, edit, and delete employee records.
- **Data Quality Validation:** Detect missing required values, invalid email addresses, duplicate records, invalid dates, and malformed phone numbers.
- **Database:** Store employee records, validation results, and import history in SQLite.
- **Search and Filtering:** Search records by name or email and filter by department or validation status.
- **Export:** Export data as CSV and quality reports and error reports as JSON.
- **Error Handling:** Display clear messages for missing files, invalid CSV files, or database errors.

## Technologies

- Python 3
- PyQt6 – Graphical user interface
- CSV – CSV file import and export
- SQLite – Persistent data storage
- JSON – Data quality reports
- Git – Version control and collaboration

## Requirements

- Python 3.10 or a compatible version agreed upon by the team
- pip
- Git

## Installation

### 1. Clone the repository
```bash
git clone <REPOSITORY-URL>
```
### 2. Navigate to the project directory
```bash
cd DataQualityManager
```
### 3. Install dependencies
```bash
pip install PyQt6
```
If a `requirements.txt` file is available, install all dependencies using:
```bash
pip install -r requirements.txt
```

## Running the Application
Start the application using:
```bash
python3 main.py

      OR

1. Create a virtual environment:
   `python3 -m venv venv`
2. Activate the environment:
   - Windows: `venv\Scripts\activate`
   - Linux/macOS: `source venv/bin/activate`
3. Install dependencies:
   `pip install -r requirements.txt`
4. Run the application:
   `python3 main.py`
```

## CSV File Format

The CSV file should contain the following columns:

```csv
first_name,last_name,email,phone,department
Max,Mustermann,max@test.de,0171234567,IT
Anna,Schmidt,anna@test.de,0171234568,HR
Peter,,peter@test.de,0171234569,IT
Max,Mustermann,max@test.de,0171234567,IT
Lisa,Meyer,invalid-email,0171234560,Sales
```

During import, missing required columns should be detected and reported to the user.

## Project Structure

The project is intended to follow a modular structure. The final structure may change during development.

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

## Data Quality Validation

The application is designed to detect common data quality issues, including:

- Missing required values
- Invalid email addresses
- Duplicate employee records
- Invalid dates
- Malformed phone numbers

The team's decision on how to handle records with errors or warnings (e.g., store, reject, or allow importing them) will be defined during development.

## Application User Interface

The application will provide a graphical interface for importing, previewing, managing, and validating employee data.

Screenshots of the application can be added here once the interface has been implemented.

## Possible Extensions

The following features are optional extensions and should not block the implementation of the core features:

- MySQL as an alternative database
- User authentication and password management
- Dashboard charts and statistics
- Configurable validation rules
- Logging
- Additional CSV import profiles