"""WTForms for portfolio application."""
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length, Email


class LoginForm(FlaskForm):
    """Admin login form."""
    
    username = StringField("Username", validators=[DataRequired(), Length(min=3)])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=6)])
    submit = SubmitField("Sign in")


class ContactForm(FlaskForm):
    """Contact form for visitors."""
    
    name = StringField("Name", validators=[DataRequired(), Length(min=2)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    subject = StringField("Subject", validators=[Length(max=255)])
    message = TextAreaField("Message", validators=[DataRequired(), Length(min=10)])
    submit = SubmitField("Send")


class SiteForm(FlaskForm):
    """Site configuration form."""
    
    name = StringField("Name", validators=[DataRequired(), Length(max=120)])
    title = StringField("Title", validators=[DataRequired(), Length(max=120)])
    tagline = TextAreaField("Tagline", validators=[DataRequired(), Length(max=255)])
    email = StringField("Email", validators=[DataRequired(), Email(), Length(max=120)])
    location = StringField("Location", validators=[Length(max=120)])
    availability = StringField("Availability", validators=[Length(max=120)])
    hero_roles = TextAreaField(
        "Hero roles",
        description="Comma-separated roles displayed in the hero section.",
        validators=[Length(max=255)],
    )
    github = StringField("GitHub URL", validators=[Length(max=255)])
    linkedin = StringField("LinkedIn URL", validators=[Length(max=255)])
    twitter = StringField("Twitter URL", validators=[Length(max=255)])
    submit = SubmitField("Save site settings")


class AboutForm(FlaskForm):
    """About section form."""
    
    headline = StringField("Headline", validators=[DataRequired(), Length(max=255)])
    paragraphs = TextAreaField(
        "Paragraphs",
        description="Enter one paragraph per line.",
        validators=[DataRequired()],
    )
    stats = TextAreaField(
        "Stats",
        description="Enter one stat per line as label|value|suffix (suffix optional).",
        validators=[Length(max=1024)],
    )
    submit = SubmitField("Save about section")


class ProjectForm(FlaskForm):
    """Project form."""
    
    slug = StringField("Slug", validators=[DataRequired(), Length(max=120)])
    title = StringField("Title", validators=[DataRequired(), Length(max=255)])
    subtitle = StringField("Subtitle", validators=[Length(max=255)])
    description = TextAreaField("Description", validators=[DataRequired()])
    tech = TextAreaField(
        "Tech stack",
        description="Enter one technology per line.",
        validators=[Length(max=1024)],
    )
    metrics = TextAreaField(
        "Metrics",
        description="Enter one metric per line as label|value.",
        validators=[Length(max=1024)],
    )
    github = StringField("GitHub URL", validators=[Length(max=255)])
    demo = StringField("Demo URL", validators=[Length(max=255)])
    status = StringField("Status", validators=[Length(max=50)])
    submit = SubmitField("Save project")


class ExperienceForm(FlaskForm):
    """Experience form."""
    
    role = StringField("Role", validators=[DataRequired(), Length(max=255)])
    company = StringField("Company", validators=[DataRequired(), Length(max=255)])
    period = StringField("Period", validators=[DataRequired(), Length(max=120)])
    location = StringField("Location", validators=[Length(max=255)])
    highlights = TextAreaField(
        "Highlights",
        description="Enter one highlight per line.",
        validators=[Length(max=1024)],
    )
    submit = SubmitField("Save experience")


class SkillForm(FlaskForm):
    """Skill category form."""
    
    category = StringField("Category", validators=[DataRequired(), Length(max=120)])
    icon = StringField("Icon", validators=[Length(max=50)])
    items = TextAreaField(
        "Items",
        description="Enter one skill/item per line.",
        validators=[Length(max=1024)],
    )
    level = StringField("Level (%)", validators=[DataRequired(), Length(max=3)])
    submit = SubmitField("Save skill category")
