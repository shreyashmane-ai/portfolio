"""Data models for portfolio application."""
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.dialects.mysql import JSON
from flask_login import UserMixin
from .extensions import db
from datetime import datetime


class User(UserMixin, db.Model):
    """Admin user for portfolio management."""
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(512), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    def set_password(self, password: str) -> None:
        """Hash and set user password."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        """Verify password against hash."""
        return check_password_hash(self.password_hash, password)

    def to_dict(self) -> dict:
        """Serialize user to dictionary (excluding password)."""
        return {"id": self.id, "username": self.username, "is_admin": self.is_admin}


class Site(db.Model):
    """Portfolio site metadata and configuration."""
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    title = db.Column(db.String(255))
    tagline = db.Column(db.Text)
    email = db.Column(db.String(255))
    location = db.Column(db.String(255))
    availability = db.Column(db.String(255))
    hero_roles = db.Column(JSON)
    social = db.Column(JSON)

    def to_dict(self) -> dict:
        """Serialize to dictionary, normalizing empty JSON fields."""
        return {
            "id": self.id,
            "name": self.name,
            "title": self.title,
            "tagline": self.tagline,
            "email": self.email,
            "location": self.location,
            "availability": self.availability,
            "hero_roles": self.hero_roles or [],
            "social": self.social or {},
        }


class About(db.Model):
    """About section content."""
    
    id = db.Column(db.Integer, primary_key=True)
    headline = db.Column(db.String(255))
    paragraphs = db.Column(JSON)
    stats = db.Column(JSON)

    def to_dict(self) -> dict:
        """Serialize to dictionary, normalizing empty JSON fields."""
        return {
            "id": self.id,
            "headline": self.headline,
            "paragraphs": self.paragraphs or [],
            "stats": self.stats or [],
        }


class SkillCategory(db.Model):
    """Skill category with proficiency level."""
    
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(120))
    icon = db.Column(db.String(50))
    items = db.Column(JSON)
    level = db.Column(db.Integer)

    def to_dict(self) -> dict:
        """Serialize to dictionary, normalizing empty JSON fields."""
        return {
            "id": self.id,
            "category": self.category,
            "icon": self.icon,
            "items": self.items or [],
            "level": self.level,
        }


class Project(db.Model):
    """Portfolio project entry."""
    
    id = db.Column(db.String(100), primary_key=True)
    slug = db.Column(db.String(120), unique=True, index=True)
    title = db.Column(db.String(255))
    subtitle = db.Column(db.String(255))
    description = db.Column(db.Text)
    tech = db.Column(JSON)
    metrics = db.Column(JSON)
    github = db.Column(db.String(255))
    demo = db.Column(db.String(255))
    status = db.Column(db.String(50))

    def to_dict(self) -> dict:
        """Serialize to dictionary, normalizing empty JSON fields."""
        return {
            "id": self.id,
            "slug": self.slug,
            "title": self.title,
            "subtitle": self.subtitle,
            "description": self.description,
            "tech": self.tech or [],
            "metrics": self.metrics or [],
            "github": self.github,
            "demo": self.demo,
            "status": self.status,
        }


class Experience(db.Model):
    """Work experience entry."""
    
    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.String(255))
    company = db.Column(db.String(255))
    period = db.Column(db.String(120))
    location = db.Column(db.String(255))
    highlights = db.Column(JSON)

    def to_dict(self) -> dict:
        """Serialize to dictionary, normalizing empty JSON fields."""
        return {
            "id": self.id,
            "role": self.role,
            "company": self.company,
            "period": self.period,
            "location": self.location,
            "highlights": self.highlights or [],
        }


class Message(db.Model):
    """Persisted contact message from site visitors."""

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    subject = db.Column(db.String(255))
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "subject": self.subject,
            "message": self.message,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
