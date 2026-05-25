"""Default in-memory data used when database is empty.

Provides fallback content while migrating to database-backed models.
Database values override these defaults when available.
"""
from datetime import datetime

SITE = {
    "name": "Shreyash Mane",
    "title": "Python Backend Engineer",
    "tagline": "Architecting thunder-powered systems at scale.",
    "email": "hello@shreyashmane.ai",
    "location": "Earth · Remote",
    "availability": "Open to opportunities",
    "hero_roles": [
        "API Architecture",
        "Distributed Systems",
        "Observability",
        "Cloud Infrastructure",
    ],
    "social": {
        "github": "https://github.com/shreyashmane",
        "linkedin": "https://linkedin.com/in/shreyashmane",
        "twitter": "https://twitter.com/shreyashmane",
    },
}

ABOUT = {
    "headline": "Engineer of resilient backends and cinematic reliability.",
    "paragraphs": [
        "I design and ship production-grade Python backends — APIs that survive storms, "
        "pipelines that never sleep, and observability stacks that illuminate every failure "
        "before users feel it.",
        "My work sits at the intersection of distributed systems, data engineering, and "
        "platform reliability. I treat infrastructure like Asgardian craft: precise, "
        "elegant, and built to endure.",
        "When I am not forging microservices, I contribute to open source, mentor engineers, "
        "and experiment with AI-assisted developer tooling.",
    ],
    "stats": [
        {"label": "Years Experience", "value": 5, "suffix": "+"},
        {"label": "Production APIs", "value": 40, "suffix": "+"},
        {"label": "Uptime Targets", "value": 99.9, "suffix": "%"},
        {"label": "Commits / Year", "value": 1200, "suffix": "+"},
    ],
}

SKILLS = [
    {"category": "Core Backend", "icon": "cpu", "items": ["Python", "FastAPI", "Flask", "Django REST", "Celery", "gRPC"], "level": 95},
    {"category": "Data & Storage", "icon": "database", "items": ["PostgreSQL", "MySQL", "Redis", "MongoDB", "Elasticsearch", "SQLAlchemy"], "level": 92},
    {"category": "Cloud & DevOps", "icon": "cloud", "items": ["AWS", "Docker", "Kubernetes", "Terraform", "GitHub Actions", "Nginx"], "level": 88},
    {"category": "Observability", "icon": "activity", "items": ["Prometheus", "Grafana", "OpenTelemetry", "Sentry", "ELK", "Datadog"], "level": 90},
]

PROJECTS = [
    {"id": "nexus-observatory", "title": "Nexus Observatory", "subtitle": "Unified metrics & tracing control plane", "description": "Multi-tenant observability platform aggregating Prometheus, Loki, and OpenTelemetry traces into a single command dashboard with alert routing.", "tech": ["Python", "FastAPI", "Kafka", "Prometheus", "Grafana", "PostgreSQL"], "metrics": [{"label": "Events / sec", "value": "50K"}], "github": "https://github.com/shreyashmane", "demo": "#", "status": "live"},
]

EXPERIENCE = [
    {"role": "Senior Python Backend Engineer", "company": "Nebula Systems", "period": "2023 — Present", "location": "Remote", "highlights": ["Led migration of monolith to 12 microservices; reduced deploy time by 70%."]},
]


def current_year() -> int:
    """Get current year for copyright notices."""
    return datetime.now().year
