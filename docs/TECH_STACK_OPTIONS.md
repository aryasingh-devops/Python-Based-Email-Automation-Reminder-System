# 2️⃣ Tech Stack Options Analysis & Recommendation

---

## 🛠️ Comparison of Architectural Approaches

To cater to varying project complexities and industry demands, here are three architectural approaches:

| Dimension | Option A: Easy (Beginner Script) | Option B: Intermediate (Modular Enterprise Project) — **SELECTED** | Option C: Advanced (Distributed Microservice) |
| :--- | :--- | :--- | :--- |
| **Target Audience** | Weekend hobbyist / Single-use script | College Student / Junior-to-Mid Developer Portfolio | Senior Distributed Systems Engineer |
| **Programming Language** | Python 3.x | Python 3.12+ | Python 3.12+ / Go / Rust |
| **Data Ingestion** | Native `csv` module | `pandas` (schema validation, relational joins, sanitation) | SQLAlchemy / PostgreSQL / Redis Streams |
| **Templating** | String `.format()` or f-strings | Modular `TemplateEngine` with HTML5 inline CSS & Plain Text fallbacks | Jinja2 + MJML (Responsive Email Framework) |
| **Email Transport** | Basic `smtplib.sendmail()` | Multi-part MIME (`email.mime`), STARTTLS, retry backoff, **Dry-Run Virtual Simulation** | SendGrid / AWS SES API / Celery task queue with RabbitMQ |
| **Scheduling** | `time.sleep()` loop | `schedule` library + `datetime` cron-like interval engine | Celery Beat + Redis or Kubernetes CronJobs |
| **Logging & Auditing** | Basic `print()` statements | Multi-handler `logging` (Console + Rotating files) + timestamped CSV/JSON audit trails | Elasticsearch + Logstash + Kibana (ELK) / Prometheus & Grafana |
| **User Interface** | Terminal prompts only | **Streamlit Interactive Web Dashboard** + Full CLI Flags | React.js / Next.js Admin Panel + FastAPI REST Backend |
| **Deployment Complexity** | Zero (single script) | **Low / Portable (Local or Streamlit Cloud / Docker)** | High (Docker, Docker Compose, Kubernetes, Redis, Cloud IAM) |
| **Resume & GitHub Impact** | Low (too simple, looks like tutorial code) | **High (Demonstrates architecture, error handling, simulation, web UI, compliance)** | Very High (requires external cloud billing and infra setup) |

---

## 🏆 Recommendation for Students: Why Option B is Best

**Option B (Intermediate Modular Architecture + Streamlit Dashboard + Dry-Run Simulation)** is the ideal choice for student portfolios and GitHub showcases because:

1. **No External Cloud Subscription Required**: Option C requires an AWS account or paid SendGrid API keys, which students typically do not possess. Option B includes a complete **Virtual Simulation Engine** that replicates 100% of the data pipeline, payload compilation, and audit trails without spending a single dollar.
2. **Visual "Wow" Factor for Recruiters**: Recruiters and non-technical interviewers rarely run CLI scripts from scratch. Providing an interactive **Streamlit Web Dashboard** (`app.py`) allows you to record an engaging video demo or deploy it live for one-click recruiter interaction.
3. **Engineering Rigor**: It implements real design patterns—Separation of Concerns (Data Loader vs. Template Engine vs. Dispatcher vs. Reporter), Environment Security (`.env`), and Unit Testing (`pytest`).
