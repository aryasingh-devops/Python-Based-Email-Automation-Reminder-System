"""
Template Engine Module.
Loads HTML and Plain-Text email templates, interpolates recipient and event variables,
and produces rendered messages for delivery.
"""

import re
from pathlib import Path
from typing import Dict, Any, Tuple
from src.config import TEMPLATES_DIR
from src.logger import app_logger

class TemplateEngine:
    """Handles loading and dynamic rendering of email templates."""

    def __init__(self, templates_dir: Path = TEMPLATES_DIR):
        self.templates_dir = Path(templates_dir)

    def load_raw_template(self, template_name: str, extension: str = ".html") -> str:
        """Loads raw template file content from the templates directory."""
        filename = f"{template_name}{extension}" if not template_name.endswith(extension) else template_name
        filepath = self.templates_dir / filename

        if not filepath.exists():
            app_logger.warning(f"Template {filepath} not found. Attempting generic fallback.")
            fallback_path = self.templates_dir / f"general_reminder{extension}"
            if fallback_path.exists():
                return fallback_path.read_text(encoding="utf-8")
            return f"Notification: {template_name}\nDetails: {{{{ event_name }}}} for {{{{ name }}}}"

        return filepath.read_text(encoding="utf-8")

    def render_content(self, raw_content: str, context: Dict[str, Any]) -> str:
        """
        Replaces double-bracket variables (e.g., {{ name }}) or single brackets
        with values from the context dictionary.
        """
        rendered = raw_content

        # Handle {{ variable }} and {{variable}}
        for key, value in context.items():
            pattern = re.compile(rf"\{{\{{\s*{re.escape(str(key))}\s*\}}\}}")
            rendered = pattern.sub(str(value) if value is not None else "", rendered)

        # Also support single-brace {variable} if present
        for key, value in context.items():
            pattern = re.compile(rf"\{{\s*{re.escape(str(key))}\s*\}}")
            rendered = pattern.sub(str(value) if value is not None else "", rendered)

        return rendered

    def generate_email_bodies(self, template_name: str, context: Dict[str, Any]) -> Tuple[str, str]:
        """
        Generates both HTML body and Plain-Text fallback body for an email dispatch.
        Returns: (html_body, text_body)
        """
        # Ensure fallback defaults for commonly expected template variables
        safe_context = {
            "name": "Valued Partner",
            "company": "Enterprise Partner",
            "role": "Team Member",
            "amount_due": "₹0.00",
            "invoice_no": "N/A",
            "event_name": "Scheduled Activity",
            "due_date": "Upcoming",
            "scheduled_time": "10:00 AM",
            "meeting_link": "#",
            "priority": "Normal",
            "subject": "Important Notification",
        }
        safe_context.update({k: v for k, v in context.items() if v != "" and v is not None})

        # Load and render HTML template
        raw_html = self.load_raw_template(template_name, extension=".html")
        html_rendered = self.render_content(raw_html, safe_context)

        # Load and render Plain-Text template
        raw_text = self.load_raw_template(template_name, extension=".txt")
        text_rendered = self.render_content(raw_text, safe_context)

        return html_rendered, text_rendered
