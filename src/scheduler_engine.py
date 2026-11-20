"""
Scheduler Engine Module.
Coordinates the end-to-end reminder processing cycle:
CSV Ingestion -> Template Rendering -> SMTP/Simulated Dispatch -> Status Tracking -> Reporting.
Supports one-off execution and continuous interval/cron-like scheduling.
"""

import time
import schedule
from datetime import datetime
from typing import List, Dict, Any, Optional

from src.csv_loader import CSVLoader
from src.template_engine import TemplateEngine
from src.email_dispatcher import EmailDispatcher
from src.report_generator import ReportGenerator
from src.logger import app_logger

class SchedulerEngine:
    """Orchestrates data flow, dispatch cycles, status updates, and automated scheduling."""

    def __init__(self, dry_run: bool = True):
        self.dry_run = dry_run
        self.csv_loader = CSVLoader()
        self.template_engine = TemplateEngine()
        self.dispatcher = EmailDispatcher(dry_run=self.dry_run)
        self.reporter = ReportGenerator()

    def process_pending_reminders(self) -> Dict[str, Any]:
        """
        Executes a complete single-pass cycle:
        1. Fetch pending reminders merged with contact details
        2. Personalize templates for each recipient
        3. Dispatch email (Live or Dry-Run)
        4. Update status in CSV
        5. Generate comprehensive audit report
        """
        cycle_start = time.time()
        app_logger.info("=" * 60)
        app_logger.info(f"Starting Email Automation Cycle [Mode: {'DRY-RUN SIMULATION' if self.dry_run else 'LIVE SMTP'}]")
        app_logger.info("=" * 60)

        # 1. Fetch dispatch queue
        queue = self.csv_loader.get_dispatch_queue(status_filter="Pending")

        if not queue:
            app_logger.info("No pending reminders found in queue. Automation cycle idle.")
            return {
                "total_processed": 0,
                "successful": 0,
                "failed": 0,
                "success_rate_pct": 0.0,
                "results": []
            }

        dispatch_results: List[Dict[str, Any]] = []

        # 2. Iterate and process each item
        for idx, item in enumerate(queue, start=1):
            reminder_id = item.get("reminder_id", f"REM-{idx}")
            recipient_name = item.get("name", "Recipient")
            template_name = item.get("template_name", "general_reminder")

            app_logger.info(f"Processing ({idx}/{len(queue)}): [{reminder_id}] for {recipient_name} (Template: {template_name})")

            # Render HTML and Plain-Text emails
            html_body, text_body = self.template_engine.generate_email_bodies(template_name, item)

            # Dispatch (Simulated or Live SMTP)
            result = self.dispatcher.dispatch_email(item, html_body, text_body)
            dispatch_results.append(result)

            # Update CSV status
            if result["status"] in ("SENT", "SIMULATED_SUCCESS"):
                new_status = "Simulated_Sent" if self.dry_run else "Sent"
            else:
                new_status = "Failed"

            self.csv_loader.update_reminder_status(reminder_id, new_status)

        # 3. Generate Audit Reports
        summary = self.reporter.generate_report(dispatch_results)
        summary["results"] = dispatch_results
        summary["cycle_duration_sec"] = round(time.time() - cycle_start, 2)

        app_logger.info("=" * 60)
        app_logger.info(f"Cycle Complete in {summary['cycle_duration_sec']}s! Processed: {summary['total_processed']} | "
                        f"Success: {summary['successful']} | Failed: {summary['failed']}")
        app_logger.info("=" * 60)

        return summary

    def run_interval_scheduler(self, interval_seconds: int = 30, max_cycles: Optional[int] = None):
        """
        Runs the automation scheduler in a continuous polling loop.
        Useful for simulating background enterprise daemons or cron jobs.
        """
        app_logger.info(f"Starting Recurring Automation Scheduler (Every {interval_seconds}s)...")
        schedule.every(interval_seconds).seconds.do(self.process_pending_reminders)

        # Run immediately on start
        self.process_pending_reminders()

        cycle_count = 1
        try:
            while True:
                schedule.run_pending()
                time.sleep(1)

                if max_cycles and cycle_count >= max_cycles:
                    app_logger.info(f"Reached maximum requested cycles ({max_cycles}). Scheduler stopped.")
                    break
        except KeyboardInterrupt:
            app_logger.info("Scheduler interrupted by user. Exiting cleanly.")
