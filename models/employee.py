from dataclasses import dataclass
from typing import Optional

@dataclass
class Employee:
    first_name: str
    last_name: str
    email: str
    phone: Optional[str] = None
    department: Optional[str] = None
    birth_date: Optional[str] = None
    id: Optional[int] = None
