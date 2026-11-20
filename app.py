"""
Streamlit Web Dashboard for Email Automation & Reminder System.
Interactive, industry-grade web application to manage contacts, preview templates,
execute virtual simulations or live SMTP dispatches, and analyze compliance audit reports.
"""

import streamlit as st
import pandas as pd
import time
import os
import json
from pathlib import Path

# Streamlit Page Configuration
st.set_page_config(
    page_title="Email Automation & Reminder Engine",
    page_icon="📬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%);
        padding: 24px 30px;
        border-radius: 12px;
        color: white;
        margin-bottom: 25px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    .main-header h1 {
        margin: 0;
        font-size: 28px;
        font-weight: 700;
        color: #ffffff;
    }
    .main-header p {
        margin: 5px 0 0 0;
        opacity: 0.9;
        font-size: 15px;
    }
    .badge-sim {
        background-color: #fef3c7;
        color: #92400e;
        padding: 4px 10px;
        border-radius: 6px;
        font-weight: 600;
        font-size: 13px;
        border: 1px solid #fde68a;
    }
    .badge-live {
        background-color: #d1fae5;
        color: #065f46;
        padding: 4px 10px;
        border-radius: 6px;
        font-weight: 600;
        font-size: 13px;
        border: 1px solid #a7f3d0;
    }
    .metric-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 10px;
        padding: 16px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# Imports from src package
from src.config import (
    CONTACTS_FILE,
    REMINDERS_FILE,
    OUTPUTS_DIR,
    LOGS_DIR,
    SMTP_SERVER,
    SMTP_PORT,
    SMTP_USER,
    SMTP_PASSWORD,
    DEFAULT_DRY_RUN
)
from src.csv_loader import CSVLoader
from src.template_engine import TemplateEngine
from src.scheduler_engine import SchedulerEngine
from src.report_generator import ReportGenerator

# Helpers
loader = CSVLoader()
template_engine = TemplateEngine()
reporter = ReportGenerator()

# Sidebar
st.sidebar.image("https://img.icons8.com/color/96/email-open.png", width=64)
st.sidebar.title("Automation Controls")

mode_choice = st.sidebar.radio(
    "Operational Execution Mode:",
    ["Virtual Simulation (Dry-Run)", "Live SMTP Dispatch"],
    index=0 if DEFAULT_DRY_RUN else 1,
    help="Virtual simulation performs full data loading, template compilation, validation, and logging without touching SMTP network or credentials."
)
is_dry_run = (mode_choice == "Virtual Simulation (Dry-Run)")

st.sidebar.divider()
st.sidebar.subheader("System Infrastructure")
st.sidebar.write(f"**SMTP Host:** `{SMTP_SERVER}`")
st.sidebar.write(f"**Port:** `{SMTP_PORT}` (STARTTLS)")
masked_user = SMTP_USER if "@" in SMTP_USER else "demo@automation.local"
st.sidebar.write(f"**Auth Account:** `{masked_user}`")
has_pw = bool(SMTP_PASSWORD and SMTP_PASSWORD != "your_16_char_app_password")
st.sidebar.write(f"**Credentials Configured:** {'✅ Yes' if has_pw else '⚠️ Simulation Mode Only'}")

st.sidebar.divider()
if st.sidebar.button("🔄 Reset Reminders to 'Pending'"):
    if REMINDERS_FILE.exists():
        df_r = pd.read_csv(REMINDERS_FILE)
        df_r["status"] = "Pending"
        df_r.to_csv(REMINDERS_FILE, index=False)
        st.sidebar.success("All reminder statuses reset to 'Pending'!")
        time.sleep(0.5)
        st.rerun()

# Header Banner
st.markdown("""
<div class="main-header">
    <h1>📬 Enterprise Email Automation & Reminder System</h1>
    <p>Automated Contact Ingestion • HTML/MIME Templating • Local Event Scheduling • Compliance Audit Logs</p>
</div>
""", unsafe_allow_html=True)

# Top Navigation Tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Executive Dashboard",
    "🚀 Dispatch Automation",
    "✉️ Email Template Preview",
    "👥 Contacts & Queue",
    "📈 Audit Reports & Logs"
])

# -----------------------------------------------------------------------------
# TAB 1: EXECUTIVE DASHBOARD
# -----------------------------------------------------------------------------
with tab1:
    contacts_df = loader.load_contacts()
    reminders_df = loader.load_reminders()

    total_contacts = len(contacts_df)
    total_reminders = len(reminders_df)
    pending_reminders = len(reminders_df[reminders_df["status"].str.lower() == "pending"])
    sent_reminders = len(reminders_df[reminders_df["status"].str.lower().isin(["sent", "simulated_sent"])])
    failed_reminders = len(reminders_df[reminders_df["status"].str.lower() == "failed"])

    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("Total Contacts", total_contacts, help="Active contacts loaded from data/contacts.csv")
    col2.metric("Total Reminders", total_reminders, help="Total reminder tasks loaded from data/reminders.csv")
    col3.metric("Pending Queue", pending_reminders, delta=f"{pending_reminders} Ready", delta_color="normal")
    col4.metric("Dispatched / Simulated", sent_reminders, delta="Completed", delta_color="inverse")
    col5.metric("Dispatch Failures", failed_reminders, delta=f"{failed_reminders} Issues", delta_color="inverse")

    st.divider()

    c_left, c_right = st.columns([1.2, 1])

    with c_left:
        st.subheader("Reminder Category Distribution")
        if not reminders_df.empty:
            type_counts = reminders_df["reminder_type"].value_counts().reset_index()
            type_counts.columns = ["Reminder Type", "Count"]
            st.bar_chart(type_counts.set_index("Reminder Type"), use_container_width=True)

    with c_right:
        st.subheader("Execution Status Distribution")
        if not reminders_df.empty:
            status_counts = reminders_df["status"].value_counts().reset_index()
            status_counts.columns = ["Status", "Count"]
            st.dataframe(status_counts, use_container_width=True, hide_index=True)

            mode_label = '<span class="badge-sim">SIMULATION / DRY-RUN</span>' if is_dry_run else '<span class="badge-live">LIVE SMTP</span>'
            st.markdown(f"**Current Engine Mode:** {mode_label}", unsafe_allow_html=True)
            st.info("💡 Tip: Use the 'Dispatch Automation' tab to execute single-batch cycles or preview emails.")

# -----------------------------------------------------------------------------
# TAB 2: DISPATCH AUTOMATION
# -----------------------------------------------------------------------------
with tab2:
    st.subheader("Automation Execution Station")
    st.write("Trigger automated batch processing for all pending reminders in the pipeline.")

    cur_mode_badge = "🧪 Virtual Simulation (Dry-Run Mode)" if is_dry_run else "⚡ Live SMTP Server Dispatch"
    st.info(f"Target Execution Mode: **{cur_mode_badge}**")

    queue = loader.get_dispatch_queue(status_filter="Pending")

    col_btn, col_info = st.columns([1, 2])
    with col_btn:
        run_btn = st.button("🚀 Trigger Automation Pipeline Now", type="primary", use_container_width=True)

    with col_info:
        st.write(f"Items pending execution: **{len(queue)} reminders**")

    if run_btn:
        if not queue:
            st.warning("No pending reminders found in the queue. Click 'Reset Reminders to Pending' in sidebar if you want to test again.")
        else:
            progress_bar = st.progress(0)
            status_text = st.empty()
            log_container = st.container()

            scheduler = SchedulerEngine(dry_run=is_dry_run)
            status_text.text("Ingesting contacts and compiling templates...")
            time.sleep(0.3)
            progress_bar.progress(30)

            status_text.text(f"Executing batch dispatch ({len(queue)} items)...")
            summary = scheduler.process_pending_reminders()
            progress_bar.progress(100)
            status_text.text("Batch cycle finished!")

            st.success(f"Successfully processed {summary.get('total_processed', 0)} reminders in {summary.get('cycle_duration_sec', 0)} seconds!")

            # Display results table
            if summary.get("results"):
                st.subheader("Dispatch Execution Audit Trail")
                res_df = pd.DataFrame(summary["results"])
                st.dataframe(
                    res_df[["reminder_id", "recipient_name", "recipient_email", "subject", "mode", "status", "latency_seconds"]],
                    use_container_width=True
                )

# -----------------------------------------------------------------------------
# TAB 3: EMAIL TEMPLATE PREVIEW
# -----------------------------------------------------------------------------
with tab3:
    st.subheader("Live Email Personalization & Rendering Preview")
    st.write("Inspect how the template engine compiles variables for each individual recipient.")

    all_queue = loader.get_dispatch_queue(status_filter=None)

    if all_queue:
        reminder_options = {f"[{item['reminder_id']}] {item['name']} - {item['reminder_type']}": idx for idx, item in enumerate(all_queue)}
        selected_label = st.selectbox("Select Target Reminder to Inspect:", list(reminder_options.keys()))
        selected_item = all_queue[reminder_options[selected_label]]

        template_name = selected_item.get("template_name", "general_reminder")
        html_rendered, text_rendered = template_engine.generate_email_bodies(template_name, selected_item)

        st.write(f"**Subject:** `{selected_item.get('subject')}`")
        st.write(f"**Recipient:** `{selected_item.get('name')} <{selected_item.get('email')}>` | **Company:** `{selected_item.get('company')}`")

        preview_col1, preview_col2 = st.columns([1.3, 1])

        with preview_col1:
            st.markdown("#### Responsive HTML Email View")
            st.components.v1.html(html_rendered, height=520, scrolling=True)

        with preview_col2:
            st.markdown("#### RFC Fallback Plain-Text View")
            st.text_area("Plain Text Content", text_rendered, height=450, disabled=True)
    else:
        st.info("No reminder records available to preview.")

# -----------------------------------------------------------------------------
# TAB 4: CONTACTS & QUEUE
# -----------------------------------------------------------------------------
with tab4:
    col_t1, col_t2 = st.columns(2)
    with col_t1:
        st.subheader("Contacts Database (`data/contacts.csv`)")
        c_df = loader.load_contacts()
        st.dataframe(c_df, use_container_width=True, hide_index=True)

    with col_t2:
        st.subheader("Reminders Schedule (`data/reminders.csv`)")
        r_df = loader.load_reminders()
        st.dataframe(r_df, use_container_width=True, hide_index=True)

# -----------------------------------------------------------------------------
# TAB 5: AUDIT REPORTS & LOGS
# -----------------------------------------------------------------------------
with tab5:
    st.subheader("Enterprise Compliance & Audit Trails")

    latest_report = reporter.get_latest_report()
    if not latest_report.empty:
        st.markdown("#### Most Recent Batch Dispatch Report")
        st.dataframe(latest_report, use_container_width=True)

        csv_bytes = latest_report.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="📥 Download Latest Audit Report (CSV)",
            data=csv_bytes,
            file_name="latest_email_dispatch_audit_report.csv",
            mime="text/csv",
            type="primary"
        )
    else:
        st.info("No dispatch reports generated yet. Execute a run from the Dispatch Automation tab.")

    st.divider()
    st.subheader("System Event Logs (`logs/system.log`)")
    sys_log_path = LOGS_DIR / "system.log"
    if sys_log_path.exists():
        log_text = sys_log_path.read_text(encoding="utf-8")
        st.text_area("Live System Log Stream", log_text[-2500:] if len(log_text) > 2500 else log_text, height=220, disabled=True)
    else:
        st.write("Logs will appear once automation cycles run.")
