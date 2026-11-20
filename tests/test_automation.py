"""
Unit and Integration Test Suite for Email Automation & Reminder System.
Rigorously audits data ingestion, template compiling, dispatcher simulation,
and compliance reporting.
"""

import pytest
import pandas as pd
from pathlib import Path
import tempfile
import os

from src.csv_loader import CSVLoader
from src.template_engine import TemplateEngine
from src.email_dispatcher import EmailDispatcher
from src.report_generator import ReportGenerator
from src.scheduler_engine import SchedulerEngine
from src.config import BASE_DIR, DATA_DIR, TEMPLATES_DIR

class TestDataIngestion:
    """Tests loading, schema validation, and joining."""

    def test_load_contacts(self):
        loader = CSVLoader()
        df = loader.load_contacts()
        assert not df.empty
        assert "contact_id" in df.columns
        assert "email" in df.columns
        assert len(df) >= 5

    def test_load_reminders(self):
        loader = CSVLoader()
        df = loader.load_reminders()
        assert not df.empty
        assert "reminder_id" in df.columns
        assert "status" in df.columns

    def test_email_validation(self):
        assert CSVLoader.validate_email_address("valid.user@example.com") is True
        assert CSVLoader.validate_email_address("invalid-email.com") is False
        assert CSVLoader.validate_email_address("") is False
        assert CSVLoader.validate_email_address(None) is False

    def test_get_dispatch_queue(self):
        loader = CSVLoader()
        queue = loader.get_dispatch_queue(status_filter=None)
        assert len(queue) > 0
        first = queue[0]
        assert "name" in first
        assert "email" in first
        assert "template_name" in first

class TestTemplateEngine:
    """Tests variable interpolation and fallback handling."""

    def test_render_content(self):
        engine = TemplateEngine()
        raw = "Hello {{ name }}, your balance of {{ amount }} is due on {{ date }}."
        context = {"name": "Alice", "amount": "$500", "date": "2026-12-01"}
        rendered = engine.render_content(raw, context)
        assert rendered == "Hello Alice, your balance of $500 is due on 2026-12-01."

    def test_generate_email_bodies(self):
        engine = TemplateEngine()
        context = {
            "name": "Bob Smith",
            "company": "Acme Corp",
            "invoice_no": "INV-999",
            "amount_due": "₹25000",
            "due_date": "2026-12-15",
            "event_name": "Cloud Audit",
            "priority": "High",
            "meeting_link": "https://example.com/pay"
        }
        html, text = engine.generate_email_bodies("payment_reminder", context)
        assert "Bob Smith" in html
        assert "Bob Smith" in text
        assert "INV-999" in html
        assert "₹25000" in html
        assert "<html" in html.lower()

class TestEmailDispatcher:
    """Tests MIME message generation and simulation mode."""

    def test_mime_generation(self):
        dispatcher = EmailDispatcher(dry_run=True)
        msg = dispatcher.build_mime_message(
            recipient_email="test@domain.com",
            recipient_name="Tester",
            subject="Test Subject",
            html_content="<p>Test HTML</p>",
            text_content="Test Plain Text",
            priority="High"
        )
        assert msg["To"] == "Tester <test@domain.com>"
        assert msg["Subject"] == "Test Subject"
        assert msg["X-Priority"] == "1"

    def test_dry_run_dispatch_success(self):
        dispatcher = EmailDispatcher(dry_run=True)
        item = {
            "reminder_id": "TEST-101",
            "contact_id": "C999",
            "name": "Jane Doe",
            "email": "jane.doe@example.com",
            "subject": "System Verification",
            "template_name": "general_reminder",
            "priority": "Normal"
        }
        result = dispatcher.dispatch_email(item, "<p>Hi Jane</p>", "Hi Jane")
        assert result["status"] == "SIMULATED_SUCCESS"
        assert result["mode"] == "DRY_RUN"
        assert result["reminder_id"] == "TEST-101"

    def test_invalid_email_dispatch_failure(self):
        dispatcher = EmailDispatcher(dry_run=True)
        item = {
            "reminder_id": "TEST-102",
            "contact_id": "C999",
            "name": "Corrupt User",
            "email": "bad-email-address",
            "subject": "System Verification"
        }
        result = dispatcher.dispatch_email(item, "<p>Hi</p>", "Hi")
        assert result["status"] == "FAILED"
        assert "Invalid email format" in result["error_message"]

class TestReportingAndScheduling:
    """Tests audit report compilation and end-to-end pipeline execution."""

    def test_report_generation(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            reporter = ReportGenerator(output_dir=Path(tmpdir))
            results = [
                {
                    "reminder_id": "REM-1",
                    "contact_id": "C1",
                    "recipient_name": "User 1",
                    "recipient_email": "u1@test.com",
                    "subject": "Test",
                    "timestamp": "2026-11-19 12:00:00",
                    "mode": "DRY_RUN",
                    "status": "SIMULATED_SUCCESS",
                    "error_message": "None",
                    "latency_seconds": 0.05
                },
                {
                    "reminder_id": "REM-2",
                    "contact_id": "C2",
                    "recipient_name": "User 2",
                    "recipient_email": "u2@test.com",
                    "subject": "Test 2",
                    "timestamp": "2026-11-19 12:00:01",
                    "mode": "DRY_RUN",
                    "status": "FAILED",
                    "error_message": "Bad address",
                    "latency_seconds": 0.01
                }
            ]
            summary = reporter.generate_report(results)
            assert summary["total_processed"] == 2
            assert summary["successful"] == 1
            assert summary["failed"] == 1
            assert summary["success_rate_pct"] == 50.0

            # Verify files were created
            created_files = list(Path(tmpdir).glob("*.csv"))
            assert len(created_files) >= 1

    def test_scheduler_cycle_dry_run(self):
        scheduler = SchedulerEngine(dry_run=True)
        summary = scheduler.process_pending_reminders()
        assert "total_processed" in summary
        assert "successful" in summary
