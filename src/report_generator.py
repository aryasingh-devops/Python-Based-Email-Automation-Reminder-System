"""
Report Generator Module.
Consolidates email dispatch results, computes metrics, and produces timestamped
CSV audit reports and analytics summaries in the outputs/ directory.
"""

import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any
import pandas as pd
from src.config import OUTPUTS_DIR
from src.logger import app_logger

class ReportGenerator:
    """Generates compliance audit trails and executive analytics reports."""

    def __init__(self, output_dir: Path = OUTPUTS_DIR):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def generate_report(self, dispatch_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Processes dispatch results list, writes timestamped CSV, and returns metrics summary.
        """
        if not dispatch_results:
            app_logger.warning("No dispatch records available to generate report.")
            return {
                "total_processed": 0,
                "successful": 0,
                "failed": 0,
                "success_rate_pct": 0.0,
                "csv_path": None
            }

        df = pd.DataFrame(dispatch_results)

        timestamp_slug = datetime.now().strftime("%Y%m%d_%H%M%S")
        csv_filename = f"dispatch_report_{timestamp_slug}.csv"
        csv_filepath = self.output_dir / csv_filename
        latest_filepath = self.output_dir / "latest_dispatch_report.csv"

        # Write reports
        df.to_csv(csv_filepath, index=False)
        df.to_csv(latest_filepath, index=False)

        # Calculate metrics
        total = len(df)
        success_count = int(df["status"].isin(["SENT", "SIMULATED_SUCCESS"]).sum())
        failed_count = int((df["status"] == "FAILED").sum())
        success_rate = round((success_count / total * 100), 2) if total > 0 else 0.0
        avg_latency = round(float(df["latency_seconds"].mean()), 3) if "latency_seconds" in df.columns else 0.0

        summary = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "total_processed": total,
            "successful": success_count,
            "failed": failed_count,
            "success_rate_pct": success_rate,
            "average_latency_sec": avg_latency,
            "report_file": csv_filename,
            "report_path": str(csv_filepath)
        }

        # Save summary JSON
        summary_json_path = self.output_dir / "summary_analytics.json"
        with open(summary_json_path, "w", encoding="utf-8") as f:
            json.dump(summary, f, indent=4)

        app_logger.info(
            f"Audit report generated: {csv_filename} | Total: {total} | "
            f"Success: {success_count} ({success_rate}%) | Failed: {failed_count}"
        )
        return summary

    def get_latest_report(self) -> pd.DataFrame:
        """Retrieves the most recent dispatch report DataFrame if available."""
        latest = self.output_dir / "latest_dispatch_report.csv"
        if latest.exists():
            return pd.read_csv(latest)
        return pd.DataFrame()
