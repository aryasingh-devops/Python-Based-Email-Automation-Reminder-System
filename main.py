"""
Main CLI Orchestration Entrypoint for Email Automation & Reminder System.
Supports single-batch runs, recurring scheduler loops, data resets, and template previews.
"""

import sys
import argparse
import pandas as pd
from datetime import datetime

from src.config import DEFAULT_DRY_RUN, REMINDERS_FILE, CONTACTS_FILE
from src.scheduler_engine import SchedulerEngine
from src.template_engine import TemplateEngine
from src.csv_loader import CSVLoader
from src.report_generator import ReportGenerator
from src.logger import app_logger

BANNER = r"""
======================================================================
  ____  _   _ _____ _   _  ___  _   _   _____ __  __    _    ___ _     
 |  _ \| | | |_   _| | | |/ _ \| \ | | | ____|  \/  |  / \  |_ _| |    
 | |_) | |_| | | | | |_| | | | |  \| | |  _| | |\/| | / _ \  | || |    
 |  __/|  _  | | | |  _  | |_| | |\  | | |___| |  | |/ ___ \ | || |___ 
 |_|   |_| |_| |_| |_| |_|\___/|_| \_| |_____|_|  |_/_/   \_\___|_____|
               AUTOMATION & REMINDER DISPATCH ENGINE
======================================================================
"""

def print_banner():
    print(BANNER)

def reset_reminder_statuses():
    """Resets all reminder statuses in reminders.csv back to 'Pending' for testing."""
    if REMINDERS_FILE.exists():
        df = pd.read_csv(REMINDERS_FILE)
        df["status"] = "Pending"
        df.to_csv(REMINDERS_FILE, index=False)
        print("[SUCCESS] All reminder statuses in data/reminders.csv reset to 'Pending'.")
    else:
        print("[ERROR] reminders.csv not found.")

def preview_templates():
    """Prints a terminal preview of rendered templates for queued reminders."""
    loader = CSVLoader()
    engine = TemplateEngine()
    queue = loader.get_dispatch_queue(status_filter=None)

    print("\n" + "=" * 60)
    print("TEMPLATE PREVIEW CONSOLE")
    print("=" * 60)

    for item in queue[:3]:  # Preview first 3
        html, text = engine.generate_email_bodies(item.get("template_name", "general_reminder"), item)
        print(f"\n[ID: {item.get('reminder_id')}] To: {item.get('name')} <{item.get('email')}>")
        print(f"Subject: {item.get('subject')}")
        print("-" * 50)
        print("PLAIN TEXT BODY PREVIEW:")
        print(text.strip())
        print("=" * 60)

def show_summary():
    """Displays the latest report metrics."""
    reporter = ReportGenerator()
    latest_df = reporter.get_latest_report()
    if latest_df.empty:
        print("[INFO] No dispatch report found in outputs/ yet. Run a dispatch cycle first.")
        return

    print("\n" + "=" * 60)
    print("LATEST DISPATCH AUDIT REPORT SUMMARY")
    print("=" * 60)
    print(latest_df[["reminder_id", "recipient_name", "recipient_email", "mode", "status", "latency_seconds"]].to_string(index=False))
    print("=" * 60)

def main():
    print_banner()

    parser = argparse.ArgumentParser(
        description="Enterprise Python Email Automation & Reminder System"
    )
    mode_group = parser.add_mutually_exclusive_group()
    mode_group.add_argument(
        "--dry-run",
        action="store_true",
        help="Run in virtual simulation mode (zero credentials, zero risk, full audit logs)"
    )
    mode_group.add_argument(
        "--live",
        action="store_true",
        help="Run in live SMTP mode (dispatches real emails via configured SMTP server)"
    )

    parser.add_argument(
        "--once",
        action="store_true",
        help="Process all pending reminders once and exit (default behavior)"
    )
    parser.add_argument(
        "--schedule",
        action="store_true",
        help="Run continuously on an automated interval loop"
    )
    parser.add_argument(
        "--interval",
        type=int,
        default=30,
        help="Polling interval in seconds for scheduled mode (default: 30)"
    )
    parser.add_argument(
        "--reset-data",
        action="store_true",
        help="Reset reminder statuses to 'Pending' for testing"
    )
    parser.add_argument(
        "--preview",
        action="store_true",
        help="Preview rendered email templates without sending"
    )
    parser.add_argument(
        "--report",
        action="store_true",
        help="Display the latest dispatch audit report"
    )

    args = parser.parse_args()

    if args.reset_data:
        reset_reminder_statuses()
        return

    if args.preview:
        preview_templates()
        return

    if args.report:
        show_summary()
        return

    # Determine dry-run mode
    if args.live:
        dry_run = False
    elif args.dry_run:
        dry_run = True
    else:
        dry_run = DEFAULT_DRY_RUN

    print(f">> Operational Mode: {'[SIMULATION / DRY-RUN]' if dry_run else '[LIVE SMTP DISPATCH]'}")
    scheduler = SchedulerEngine(dry_run=dry_run)

    if args.schedule:
        print(f">> Starting recurring scheduler with interval: {args.interval}s")
        scheduler.run_interval_scheduler(interval_seconds=args.interval)
    else:
        print(">> Executing single batch pass for all pending reminders...")
        summary = scheduler.process_pending_reminders()
        print("\n>> BATCH EXECUTION SUMMARY:")
        print(f"   Total Processed: {summary.get('total_processed', 0)}")
        print(f"   Success Count:   {summary.get('successful', 0)}")
        print(f"   Failure Count:   {summary.get('failed', 0)}")
        print(f"   Success Rate:    {summary.get('success_rate_pct', 0.0)}%")
        if summary.get("report_file"):
            print(f"   Audit Report:    outputs/{summary.get('report_file')}")
        print("\n[Done] System executed successfully.")

if __name__ == "__main__":
    main()
