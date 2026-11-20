import re
from datetime import datetime
from models.employee import Employee
from models.validation_result import ValidationResult

EMAIL_REGEX = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
PHONE_REGEX = re.compile(r"^\+?[0-9\s\-()]{6,20}$")


def validate_records(records: list[Employee]) -> list[ValidationResult]:
    results: list[ValidationResult] = []
    seen_records: set[tuple[str, str, str]] = set()

    for idx, emp in enumerate(records, start=1):
        # Required fields check
        if not emp.first_name.strip():
            results.append(ValidationResult("first_name", "First name is required.", "ERROR", emp.id, idx))
        if not emp.last_name.strip():
            results.append(ValidationResult("last_name", "Last name is required.", "ERROR", emp.id, idx))

        # Email format check
        email_clean = emp.email.strip()
        if not email_clean:
            results.append(ValidationResult("email", "Email is required.", "ERROR", emp.id, idx))
        elif not EMAIL_REGEX.match(email_clean):
            results.append(ValidationResult("email", f"Invalid email format: '{email_clean}'.", "ERROR", emp.id, idx))

        # Phone format check (optional field)
        if emp.phone and emp.phone.strip():
            if not PHONE_REGEX.match(emp.phone.strip()):
                results.append(ValidationResult("phone", f"Invalid phone format: '{emp.phone}'.", "ERROR", emp.id, idx))
                return
        # Birth date check (optional field, YYYY-MM-DD)
        if emp.birth_date and emp.birth_date.strip():
            try:
                datetime.strptime(emp.birth_date.strip(), "%Y-%m-%d")
            except ValueError:
                results.append(ValidationResult("birth_date", f"Invalid date (expected YYYY-MM-DD): '{emp.birth_date}'.", "ERROR", emp.id, idx))

        # Duplicate check
        identity = (emp.first_name.strip().lower(), emp.last_name.strip().lower(), email_clean.lower())
        if identity in seen_records:
            results.append(ValidationResult("email", f"Duplicate record detected for {emp.first_name} {emp.last_name}.", "WARNING", emp.id, idx))
        else:
            seen_records.add(identity)

    return results
