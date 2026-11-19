from dataclasses import dataclass
from typing import Optional

@dataclass
class ValidationResult:
    column_name: str
    error_message: str
    severity: str  # "ERROR" or "WARNING"
    employee_id: Optional[int] = None
    row_index: Optional[int] = None
    id: Optional[int] = None
