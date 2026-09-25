import enum
from datetime import date

from app import db


class Status(enum.Enum):
    APPLIED = "APPLIED"
    INTERVIEW = "INTERVIEW"
    OFFER = "OFFER"
    REJECTED = "REJECTED"


class Application(db.Model):
    __tablename__ = "applications"

    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(120))
    status = db.Column(db.Enum(Status), default=Status.APPLIED, nullable=False)
    applied_date = db.Column(db.Date, default=date.today)
    reminder_date = db.Column(db.Date, nullable=True)
    notes = db.Column(db.Text, nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "company_name": self.company_name,
            "role": self.role,
            "status": self.status.value,
            "applied_date": self.applied_date.isoformat() if self.applied_date else None,
            "reminder_date": self.reminder_date.isoformat() if self.reminder_date else None,
            "notes": self.notes,
        }
