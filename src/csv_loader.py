"""
CSV Data Loading & Validation Module.
Handles ingestion, schema validation, data sanitation, and relational joining of contacts and reminders.
"""

import re
import pandas as pd
from typing import Dict, List, Optional, Tuple
from pathlib import Path
from src.config import CONTACTS_FILE, REMINDERS_FILE
from src.logger import app_logger

# Regular expression for basic email format validation
EMAIL_REGEX = re.compile(r"^[\w\.-]+@[\w\.-]+\.\w+$")

REQUIRED_CONTACT_COLUMNS = ["contact_id", "name", "email", "company", "role", "status"]
REQUIRED_REMINDER_COLUMNS = [
    "reminder_id", "contact_id", "reminder_type", "subject",
    "template_name", "due_date", "scheduled_time", "status"
]

class CSVLoader:
    """Manages reading, validating, and updating CSV files for the automation system."""

    def __init__(self, contacts_path: Path = CONTACTS_FILE, reminders_path: Path = REMINDERS_FILE):
        self.contacts_path = Path(contacts_path)
        self.reminders_path = Path(reminders_path)

    def load_contacts(self) -> pd.DataFrame:
        """Loads and validates contact records."""
        if not self.contacts_path.exists():
            app_logger.error(f"Contacts file not found: {self.contacts_path}")
            raise FileNotFoundError(f"Contacts file missing at {self.contacts_path}")

        try:
            df = pd.read_csv(self.contacts_path, dtype=str).fillna("")
            df.columns = [col.strip() for col in df.columns]
            for col in df.select_dtypes(include="object").columns:
                df[col] = df[col].str.strip()

            # Schema validation
            missing_cols = [col for col in REQUIRED_CONTACT_COLUMNS if col not in df.columns]
            if missing_cols:
                raise ValueError(f"Contacts CSV missing required columns: {missing_cols}")

            app_logger.info(f"Loaded {len(df)} contacts from {self.contacts_path.name}")
            return df
        except Exception as e:
            app_logger.error(f"Error loading contacts CSV: {e}")
            raise

    def load_reminders(self) -> pd.DataFrame:
        """Loads and validates reminder records."""
        if not self.reminders_path.exists():
            app_logger.error(f"Reminders file not found: {self.reminders_path}")
            raise FileNotFoundError(f"Reminders file missing at {self.reminders_path}")

        try:
            df = pd.read_csv(self.reminders_path, dtype=str).fillna("")
            df.columns = [col.strip() for col in df.columns]
            for col in df.select_dtypes(include="object").columns:
                df[col] = df[col].str.strip()

            missing_cols = [col for col in REQUIRED_REMINDER_COLUMNS if col not in df.columns]
            if missing_cols:
                raise ValueError(f"Reminders CSV missing required columns: {missing_cols}")

            app_logger.info(f"Loaded {len(df)} reminders from {self.reminders_path.name}")
            return df
        except Exception as e:
            app_logger.error(f"Error loading reminders CSV: {e}")
            raise

    def get_dispatch_queue(self, status_filter: Optional[str] = "Pending") -> List[Dict]:
        """
        Merges contacts with reminders to construct a rich, actionable dispatch queue.
        Filters by reminder status if specified (e.g. 'Pending').
        """
        contacts_df = self.load_contacts()
        reminders_df = self.load_reminders()

        # Join datasets on contact_id
        merged_df = pd.merge(
            reminders_df,
            contacts_df,
            on="contact_id",
            how="inner",
            suffixes=("_rem", "_con")
        )

        if status_filter:
            merged_df = merged_df[merged_df["status_rem"].str.lower() == status_filter.lower()]

        # Convert to dictionary records
        queue = merged_df.to_dict(orient="records")
        app_logger.info(f"Built dispatch queue with {len(queue)} items (filter: {status_filter})")
        return queue

    @staticmethod
    def validate_email_address(email: str) -> bool:
        """Returns True if the email syntax is valid, else False."""
        if not email or not isinstance(email, str):
            return False
        return bool(EMAIL_REGEX.match(email.strip()))

    def update_reminder_status(self, reminder_id: str, new_status: str) -> bool:
        """Updates the status column for a given reminder_id in reminders.csv."""
        try:
            df = self.load_reminders()
            mask = df["reminder_id"] == reminder_id
            if not mask.any():
                app_logger.warning(f"Reminder ID {reminder_id} not found for status update.")
                return False

            df.loc[mask, "status"] = new_status
            df.to_csv(self.reminders_path, index=False)
            app_logger.info(f"Updated {reminder_id} status to '{new_status}' in {self.reminders_path.name}")
            return True
        except Exception as e:
            app_logger.error(f"Failed to update status for {reminder_id}: {e}")
            return False
