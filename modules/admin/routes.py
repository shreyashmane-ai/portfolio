"""Admin panel routes for portfolio management."""
from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required
from ..forms import SiteForm, AboutForm, ProjectForm, ExperienceForm, SkillForm
from ..models import Site, About, Project, Experience, SkillCategory, Message
from ..extensions import db
from ..utils import safe_lines, parse_metrics

bp = Blueprint("admin", __name__, url_prefix="/admin")


def _format_metrics(metrics_list: list | None) -> str:
    """Format metrics list back to pipe-separated string."""
    if not metrics_list:
        return ""
    return "\n".join(
        f"{m.get('label', '')}|{m.get('value', '')}" + (f"|{m.get('suffix', '')}" if m.get('suffix') else "")
        for m in metrics_list
    )



@bp.route("/")
@login_required
def index():
    site = Site.query.first()
    about = About.query.first()
    projects = Project.query.all()
    experience = Experience.query.all()
    skills = SkillCategory.query.all()
    return render_template(
        "admin/index.html",
        site=site,
        about=about,
        projects=projects,
        experience=experience,
        skills=skills,
    )



@bp.route("/messages")
@login_required
def message_list():
    messages = Message.query.order_by(Message.created_at.desc()).all()
    return render_template("admin/messages.html", messages=messages)


@bp.route("/messages/<int:message_id>")
@login_required
def message_view(message_id):
    msg = Message.query.get_or_404(message_id)    
    return render_template("admin/message_detail.html", message=msg)


@bp.route("/messages/<int:message_id>/delete", methods=["POST"])
@login_required
def message_delete(message_id):
    msg = Message.query.get_or_404(message_id)
    db.session.delete(msg)
    db.session.commit()
    flash("Message deleted.", "success")
    return redirect(url_for("admin.message_list"))


@bp.route("/site", methods=["GET", "POST"])
@login_required
def site_settings():
    site = Site.query.first() or Site()
    form = SiteForm()

    if request.method == "GET" and site.id:
        form.name.data = site.name
        form.title.data = site.title
        form.tagline.data = site.tagline
        form.email.data = site.email
        form.location.data = site.location
        form.availability.data = site.availability
        form.hero_roles.data = ", ".join(site.hero_roles or [])
        form.github.data = site.social.get("github", "") if site.social else ""
        form.linkedin.data = site.social.get("linkedin", "") if site.social else ""
        form.twitter.data = site.social.get("twitter", "") if site.social else ""

    if form.validate_on_submit():
        if not site.id:
            db.session.add(site)

        site.name = form.name.data
        site.title = form.title.data
        site.tagline = form.tagline.data
        site.email = form.email.data
        site.location = form.location.data
        site.availability = form.availability.data
        site.hero_roles = [role.strip() for role in form.hero_roles.data.split(",") if role.strip()]
        site.social = {
            "github": form.github.data,
            "linkedin": form.linkedin.data,
            "twitter": form.twitter.data,
        }

        db.session.commit()
        flash("Site settings saved.", "success")
        return redirect(url_for("admin.site_settings"))

    return render_template("admin/site.html", form=form, site=site)


@bp.route("/about", methods=["GET", "POST"])
@login_required
def about_settings():
    about = About.query.first() or About()
    form = AboutForm()

    if request.method == "GET" and about.id:
        form.headline.data = about.headline
        form.paragraphs.data = "\n".join(about.paragraphs or [])
        form.stats.data = "\n".join(
            f"{stat.get('label','')}|{stat.get('value','')}|{stat.get('suffix','')}".rstrip("|")
            for stat in (about.stats or [])
        )

    if form.validate_on_submit():
        if not about.id:
            db.session.add(about)

        about.headline = form.headline.data
        about.paragraphs = safe_lines(form.paragraphs.data)
        about.stats = parse_metrics(form.stats.data)

        db.session.commit()
        flash("About section updated.", "success")
        return redirect(url_for("admin.about_settings"))

    return render_template("admin/about.html", form=form, about=about)


@bp.route("/projects")
@login_required
def project_list():
    projects = Project.query.order_by(Project.title).all()
    return render_template("admin/projects.html", projects=projects)


@bp.route("/projects/new", methods=["GET", "POST"])
@login_required
def project_create():
    form = ProjectForm()
    if form.validate_on_submit():
        project = Project(
            id=form.slug.data,
            slug=form.slug.data,
            title=form.title.data,
            subtitle=form.subtitle.data,
            description=form.description.data,
            tech=safe_lines(form.tech.data),
            metrics=parse_metrics(form.metrics.data),
            github=form.github.data,
            demo=form.demo.data,
            status=form.status.data,
        )
        db.session.add(project)
        db.session.commit()
        flash("Project created.", "success")
        return redirect(url_for("admin.project_list"))
    return render_template("admin/project_form.html", form=form, project=None)


@bp.route("/projects/<string:project_id>/edit", methods=["GET", "POST"])
@login_required
def project_edit(project_id):
    project = Project.query.get_or_404(project_id)
    form = ProjectForm()
    if request.method == "GET":
        form.slug.data = project.slug
        form.title.data = project.title
        form.subtitle.data = project.subtitle
        form.description.data = project.description
        form.tech.data = "\n".join(project.tech or [])
        form.metrics.data = "\n".join(f"{item.get('label','')}|{item.get('value','')}" for item in (project.metrics or []))
        form.github.data = project.github
        form.demo.data = project.demo
        form.status.data = project.status

    if form.validate_on_submit():
        project.slug = form.slug.data
        project.title = form.title.data
        project.subtitle = form.subtitle.data
        project.description = form.description.data
        project.tech = safe_lines(form.tech.data)
        project.metrics = parse_metrics(form.metrics.data)
        project.github = form.github.data
        project.demo = form.demo.data
        project.status = form.status.data
        db.session.commit()
        flash("Project updated.", "success")
        return redirect(url_for("admin.project_list"))
    return render_template("admin/project_form.html", form=form, project=project)


@bp.route("/projects/<string:project_id>/delete", methods=["POST"])
@login_required
def project_delete(project_id):
    project = Project.query.get_or_404(project_id)
    db.session.delete(project)
    db.session.commit()
    flash("Project deleted.", "success")
    return redirect(url_for("admin.project_list"))


@bp.route("/experience")
@login_required
def experience_list():
    experience = Experience.query.order_by(Experience.period.desc()).all()
    return render_template("admin/experience.html", experience=experience)


@bp.route("/experience/new", methods=["GET", "POST"])
@login_required
def experience_create():
    form = ExperienceForm()
    if form.validate_on_submit():
        exp = Experience(
            role=form.role.data,
            company=form.company.data,
            period=form.period.data,
            location=form.location.data,
            highlights=safe_lines(form.highlights.data),
        )
        db.session.add(exp)
        db.session.commit()
        flash("Experience entry created.", "success")
        return redirect(url_for("admin.experience_list"))
    return render_template("admin/experience_form.html", form=form, experience=None)


@bp.route("/experience/<int:experience_id>/edit", methods=["GET", "POST"])
@login_required
def experience_edit(experience_id):
    exp = Experience.query.get_or_404(experience_id)
    form = ExperienceForm()
    if request.method == "GET":
        form.role.data = exp.role
        form.company.data = exp.company
        form.period.data = exp.period
        form.location.data = exp.location
        form.highlights.data = "\n".join(exp.highlights or [])

    if form.validate_on_submit():
        exp.role = form.role.data
        exp.company = form.company.data
        exp.period = form.period.data
        exp.location = form.location.data
        exp.highlights = safe_lines(form.highlights.data)
        db.session.commit()
        flash("Experience entry updated.", "success")
        return redirect(url_for("admin.experience_list"))
    return render_template("admin/experience_form.html", form=form, experience=exp)


@bp.route("/experience/<int:experience_id>/delete", methods=["POST"])
@login_required
def experience_delete(experience_id):
    exp = Experience.query.get_or_404(experience_id)
    db.session.delete(exp)
    db.session.commit()
    flash("Experience entry deleted.", "success")
    return redirect(url_for("admin.experience_list"))


@bp.route("/skills")
@login_required
def skill_list():
    skills = SkillCategory.query.order_by(SkillCategory.category).all()
    return render_template("admin/skills.html", skills=skills)


@bp.route("/skills/new", methods=["GET", "POST"])
@login_required
def skill_create():
    form = SkillForm()
    if form.validate_on_submit():
        skill = SkillCategory(
            category=form.category.data,
            icon=form.icon.data,
            items=safe_lines(form.items.data),
            level=int(form.level.data or 0),
        )
        db.session.add(skill)
        db.session.commit()
        flash("Skill category created.", "success")
        return redirect(url_for("admin.skill_list"))
    return render_template("admin/skill_form.html", form=form, skill=None)


@bp.route("/skills/<int:skill_id>/edit", methods=["GET", "POST"])
@login_required
def skill_edit(skill_id):
    skill = SkillCategory.query.get_or_404(skill_id)
    form = SkillForm()
    if request.method == "GET":
        form.category.data = skill.category
        form.icon.data = skill.icon
        form.items.data = "\n".join(skill.items or [])
        form.level.data = str(skill.level)

    if form.validate_on_submit():
        skill.category = form.category.data
        skill.icon = form.icon.data
        skill.items = safe_lines(form.items.data)
        skill.level = int(form.level.data or 0)
        db.session.commit()
        flash("Skill category updated.", "success")
        return redirect(url_for("admin.skill_list"))
    return render_template("admin/skill_form.html", form=form, skill=skill)


@bp.route("/skills/<int:skill_id>/delete", methods=["POST"])
@login_required
def skill_delete(skill_id):
    skill = SkillCategory.query.get_or_404(skill_id)
    db.session.delete(skill)
    db.session.commit()
    flash("Skill category deleted.", "success")
    return redirect(url_for("admin.skill_list"))
