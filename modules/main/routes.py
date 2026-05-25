"""Main routes for portfolio display."""
from flask import Blueprint, current_app, render_template, request, redirect, url_for, flash
from ..forms import ContactForm
from ..models import Site, About, Project, Experience, SkillCategory, Message
from ..extensions import db
from ..notifications import send_contact_notification, send_confirmation_email
from flask import current_app
from .. import defaults as _defaults

bp = Blueprint("main", __name__)


@bp.app_context_processor
def inject_globals() -> dict:
    """Provide template globals from database or defaults.
    
    Prioritizes database values, falls back to defaults if unavailable.
    Always returns all expected keys for template safety.
    """
    data = {
        "site": _defaults.SITE,
        "about": _defaults.ABOUT,
        "skills": _defaults.SKILLS,
        "projects": _defaults.PROJECTS,
        "experience": _defaults.EXPERIENCE,
        "current_year": _defaults.current_year(),
    }

    try:
        # Query all data
        site = Site.query.first()
        about = About.query.first()
        skills = SkillCategory.query.all()
        projects = Project.query.all()
        experience = Experience.query.all()

        # Serialize and merge with defaults
        if site:
            data["site"] = site.to_dict()
        if about:
            data["about"] = about.to_dict()
        if skills:
            data["skills"] = [s.to_dict() for s in skills]
        if projects:
            data["projects"] = [p.to_dict() for p in projects]
        if experience:
            data["experience"] = [e.to_dict() for e in experience]

    except Exception:
        # Keep defaults if DB not available or any error occurs
        pass

    return data


@bp.route("/")
def index() -> str:
    """Render homepage with contact form."""
    form = ContactForm()
    return render_template("index.html", form=form)


@bp.route("/contact", methods=["POST"])
def contact():
    """Handle contact form submission."""
    form = ContactForm()
    if not form.validate_on_submit():
        for field, errors in form.errors.items():
            for err in errors:
                flash(err, "danger")
        return redirect(url_for("main.index") + "#contact")
    # Persist the contact message
    msg = Message(
        name=form.name.data,
        email=form.email.data,
        subject=form.subject.data,
        message=form.message.data,
    )

    try:
        db.session.add(msg)
        db.session.commit()
    except Exception:
        db.session.rollback()
        # Try creating tables (development fallback) and retry once
        try:
            db.create_all()
            db.session.add(msg)
            db.session.commit()
        except Exception:
            db.session.rollback()
            current_app.logger.exception("Failed to save contact message")
            flash("Unable to transmit right now. Please try again later.", "danger")
            return redirect(url_for("main.index") + "#contact")
    # Try sending email notification (best-effort)
    try:
        cfg = current_app.config
        send_contact_notification(msg.to_dict(), cfg)
    except Exception:
        current_app.logger.info("Contact saved but notification failed or not configured.")

    # Send confirmation email to submitter (best-effort)
    try:
        send_confirmation_email(msg.to_dict(), cfg)
    except Exception:
        current_app.logger.info("Confirmation email failed or not configured.")

    flash("Transmission received. I will respond within 24 hours.", "success")
    return redirect(url_for("main.index") + "#contact")
