import json
from dataclasses import asdict
from datetime import datetime
from pathlib import Path
from models.validation_result import ValidationResult


def export_quality_report_json(
    total_records: int,
    valid_records: int,
    findings: list[ValidationResult],
    output_path: str,
) -> None:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    error_count = sum(1 for f in findings if f.severity == "ERROR")
    warning_count = sum(1 for f in findings if f.severity == "WARNING")

    report = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "summary": {
            "total_records": total_records,
            "valid_records": valid_records,
            "errors": error_count,
            "warnings": warning_count,
        },
        "findings": [asdict(f) for f in findings],
    }

    with path.open(mode="w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
