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

    @classmethod
    def from_record(cls, record):
        if isinstance(record, cls):
            return record

        if isinstance(record, dict):
            get = record.get
        else:
            get = lambda key, default=None: getattr(record, key, default)

        return cls(
            id=get("id"),
            first_name=get("first_name", "") or "",
            last_name=get("last_name", "") or "",
            email=get("email", "") or "",
            phone=get("phone", "") or "",
            department=get("department", "") or "",
            birth_date=get("birth_date", "") or "",
        )

    def to_dict(self):
        return {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "phone": self.phone,
            "department": self.department,
            "birth_date": self.birth_date,
        }
