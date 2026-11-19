import csv
from pathlib import Path

REQUIRED_HEADERS = {"first_name", "last_name", "email", "phone", "department", "birth_date"}


def read_csv(file_path: str) -> tuple[list[dict[str, str]], list[str]]:
    path = Path(file_path)
    if not path.exists():
        return [], [f"File not found: {file_path}"]

    try:
        with path.open(mode="r", encoding="utf-8-sig", newline="") as f:
            reader = csv.DictReader(f)
            if not reader.fieldnames:
                return [], ["CSV file is empty or missing headers."]

            headers = {h.strip() for h in reader.fieldnames if h}
            missing = REQUIRED_HEADERS - headers
            if missing:
                return [], [f"Missing required columns: {', '.join(sorted(missing))}"]

            rows: list[dict[str, str]] = []
            for row in reader:
                cleaned = {k.strip(): (v.strip() if v is not None else "") for k, v in row.items() if k}
                rows.append(cleaned)
            return rows, []
    except UnicodeDecodeError:
        return [], ["Encoding error: Please save the CSV file as UTF-8."]
    except csv.Error as exc:
        return [], [f"CSV parsing error: {exc}"]
