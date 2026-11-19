import csv
from pathlib import Path
from models.employee import Employee


def export_employees_csv(employees: list[Employee], output_path: str) -> None:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = ["id", "first_name", "last_name", "email", "phone", "department", "birth_date"]

    with path.open(mode="w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for emp in employees:
            writer.writerow({
                "id": emp.id or "",
                "first_name": emp.first_name,
                "last_name": emp.last_name,
                "email": emp.email,
                "phone": emp.phone or "",
                "department": emp.department or "",
                "birth_date": emp.birth_date or "",
            })
