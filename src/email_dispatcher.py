"""
Email Dispatcher Module.
Orchestrates MIME email message construction, safe password handling,
SMTP connection lifecycle (STARTTLS / SSL), and Virtual Simulation (Dry-Run Mode).
"""

import smtplib
import socket
import time
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formatdate, make_msgid
from typing import Dict, Any, Optional

from src.config import (
    SMTP_SERVER,
    SMTP_PORT,
    SMTP_USER,
    SMTP_PASSWORD,
    SENDER_NAME,
    SMTP_USE_SSL,
    SMTP_TIMEOUT_SECONDS,
    MAX_RETRIES,
    RETRY_DELAY_SECONDS,
    DEFAULT_DRY_RUN
)
from src.logger import app_logger, dispatch_logger
from src.csv_loader import CSVLoader

class EmailDispatcher:
    """Manages secure email transmission with dual-mode operation: Live SMTP and Dry-Run Simulation."""

    def __init__(self, dry_run: bool = DEFAULT_DRY_RUN):
        self.dry_run = dry_run
        self.smtp_server = SMTP_SERVER
        self.smtp_port = SMTP_PORT
        self.smtp_user = SMTP_USER
        self.smtp_password = SMTP_PASSWORD
        self.sender_name = SENDER_NAME
        self.use_ssl = SMTP_USE_SSL

    def build_mime_message(
        self,
        recipient_email: str,
        recipient_name: str,
        subject: str,
        html_content: str,
        text_content: str,
        priority: str = "Normal"
    ) -> MIMEMultipart:
        """Constructs an RFC 5322 compliant multipart/alternative MIME message."""
        msg = MIMEMultipart("alternative")
        msg["From"] = f"{self.sender_name} <{self.smtp_user}>"
        msg["To"] = f"{recipient_name} <{recipient_email}>"
        msg["Subject"] = subject
        msg["Date"] = formatdate(localtime=True)
        msg["Message-ID"] = make_msgid(domain="automation.local")

        # Set priority headers if urgent
        if priority.lower() in ("high", "urgent", "critical"):
            msg["X-Priority"] = "1"
            msg["Importance"] = "high"

        # Attach Plain-Text part first (fallback)
        part_text = MIMEText(text_content, "plain", "utf-8")
        msg.attach(part_text)

        # Attach HTML part second (primary display for modern clients)
        part_html = MIMEText(html_content, "html", "utf-8")
        msg.attach(part_html)

        return msg

    def dispatch_email(
        self,
        item: Dict[str, Any],
        html_body: str,
        text_body: str
    ) -> Dict[str, Any]:
        """
        Dispatches a single reminder email item in either LIVE or DRY_RUN mode.
        Returns a standardized dispatch result dictionary for reporting and logging.
        """
        recipient_email = item.get("email", "").strip()
        recipient_name = item.get("name", "Valued Recipient").strip()
        subject = item.get("subject", "Automated Notification").strip()
        reminder_id = item.get("reminder_id", "N/A")
        contact_id = item.get("contact_id", "N/A")
        priority = item.get("priority", "Normal")

        start_time = time.time()
        timestamp_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Validate recipient email format
        if not CSVLoader.validate_email_address(recipient_email):
            err = f"Invalid email format: '{recipient_email}'"
            app_logger.error(f"[{reminder_id}] Dispatch rejected: {err}")
            dispatch_logger.error(f"REJECTED | {reminder_id} | {recipient_email} | {err}")
            return {
                "reminder_id": reminder_id,
                "contact_id": contact_id,
                "recipient_name": recipient_name,
                "recipient_email": recipient_email,
                "subject": subject,
                "timestamp": timestamp_str,
                "mode": "DRY_RUN" if self.dry_run else "LIVE_SMTP",
                "status": "FAILED",
                "error_message": err,
                "latency_seconds": round(time.time() - start_time, 3)
            }

        # Build message payload
        msg = self.build_mime_message(
            recipient_email=recipient_email,
            recipient_name=recipient_name,
            subject=subject,
            html_content=html_body,
            text_content=text_body,
            priority=priority
        )

        # -------------------------------------------------------------
        # BRANCH 1: DRY RUN / VIRTUAL SIMULATION MODE
        # -------------------------------------------------------------
        if self.dry_run:
            # Simulate real-world network latency (30-80ms)
            time.sleep(0.05)
            elapsed = round(time.time() - start_time, 3)
            app_logger.info(
                f"[SIMULATION] Generated email for {recipient_name} <{recipient_email}> | "
                f"Subject: '{subject}' | Template: {item.get('template_name')} | Status: SIMULATED_SUCCESS"
            )
            dispatch_logger.info(
                f"SIMULATED_SUCCESS | ID: {reminder_id} | To: {recipient_email} | Subject: {subject} | Latency: {elapsed}s"
            )
            return {
                "reminder_id": reminder_id,
                "contact_id": contact_id,
                "recipient_name": recipient_name,
                "recipient_email": recipient_email,
                "subject": subject,
                "timestamp": timestamp_str,
                "mode": "DRY_RUN",
                "status": "SIMULATED_SUCCESS",
                "error_message": "None (Virtual Simulation Passed)",
                "latency_seconds": elapsed
            }

        # -------------------------------------------------------------
        # BRANCH 2: LIVE SMTP DISPATCH MODE
        # -------------------------------------------------------------
        attempts = 0
        last_error = ""

        while attempts < MAX_RETRIES:
            attempts += 1
            try:
                app_logger.info(
                    f"Connecting to SMTP {self.smtp_server}:{self.smtp_port} "
                    f"(Attempt {attempts}/{MAX_RETRIES}) for {recipient_email}..."
                )

                if self.use_ssl:
                    server = smtplib.SMTP_SSL(self.smtp_server, self.smtp_port, timeout=SMTP_TIMEOUT_SECONDS)
                else:
                    server = smtplib.SMTP(self.smtp_server, self.smtp_port, timeout=SMTP_TIMEOUT_SECONDS)
                    server.ehlo()
                    server.starttls()
                    server.ehlo()

                # Authenticate
                server.login(self.smtp_user, self.smtp_password)

                # Send
                server.send_message(msg)
                server.quit()

                elapsed = round(time.time() - start_time, 3)
                app_logger.info(f"Successfully delivered email to {recipient_email} in {elapsed}s")
                dispatch_logger.info(
                    f"SENT | ID: {reminder_id} | To: {recipient_email} | Subject: {subject} | Latency: {elapsed}s"
                )

                return {
                    "reminder_id": reminder_id,
                    "contact_id": contact_id,
                    "recipient_name": recipient_name,
                    "recipient_email": recipient_email,
                    "subject": subject,
                    "timestamp": timestamp_str,
                    "mode": "LIVE_SMTP",
                    "status": "SENT",
                    "error_message": "Delivered successfully",
                    "latency_seconds": elapsed
                }

            except smtplib.SMTPAuthenticationError as auth_err:
                last_error = (
                    f"Authentication Error: Invalid username/password. If using Gmail, "
                    f"make sure to use a 16-character App Password (Details: {auth_err})"
                )
                app_logger.error(f"[{reminder_id}] {last_error}")
                # Auth error won't change on retry
                break

            except (smtplib.SMTPConnectError, socket.timeout, socket.gaierror) as net_err:
                last_error = f"Network/Connection Timeout to {self.smtp_server}:{self.smtp_port} ({net_err})"
                app_logger.warning(f"[{reminder_id}] Attempt {attempts} failed: {last_error}")
                if attempts < MAX_RETRIES:
                    time.sleep(RETRY_DELAY_SECONDS)

            except Exception as exc:
                last_error = f"Unexpected SMTP failure: {exc}"
                app_logger.error(f"[{reminder_id}] Error: {last_error}")
                if attempts < MAX_RETRIES:
                    time.sleep(RETRY_DELAY_SECONDS)

        # If failed after all retries
        elapsed = round(time.time() - start_time, 3)
        dispatch_logger.error(
            f"FAILED | ID: {reminder_id} | To: {recipient_email} | Reason: {last_error} | Latency: {elapsed}s"
        )
        return {
            "reminder_id": reminder_id,
            "contact_id": contact_id,
            "recipient_name": recipient_name,
            "recipient_email": recipient_email,
            "subject": subject,
            "timestamp": timestamp_str,
            "mode": "LIVE_SMTP",
            "status": "FAILED",
            "error_message": last_error,
            "latency_seconds": elapsed
        }
