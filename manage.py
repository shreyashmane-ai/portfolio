import os
import click
from app import create_app
from modules.extensions import db
from modules import defaults
from modules.models import User, Site, About, Project, Experience, SkillCategory

app = create_app()


@app.cli.command("seed-defaults")
def seed_defaults():
    """Seed the database with default portfolio content and an admin user."""
    with app.app_context():
        if not Site.query.first():
            site = Site(
                name=defaults.SITE["name"],
                title=defaults.SITE["title"],
                tagline=defaults.SITE["tagline"],
                email=defaults.SITE["email"],
                location=defaults.SITE["location"],
                availability=defaults.SITE["availability"],
                hero_roles=defaults.SITE["hero_roles"],
                social=defaults.SITE["social"],
            )
            db.session.add(site)

        if not About.query.first():
            about = About(
                headline=defaults.ABOUT["headline"],
                paragraphs=defaults.ABOUT["paragraphs"],
                stats=defaults.ABOUT["stats"],
            )
            db.session.add(about)

        if not SkillCategory.query.first():
            for skill in defaults.SKILLS:
                db.session.add(
                    SkillCategory(
                        category=skill["category"],
                        icon=skill["icon"],
                        items=skill["items"],
                        level=skill["level"],
                    )
                )

        if not Project.query.first():
            for project in defaults.PROJECTS:
                db.session.add(
                    Project(
                        slug=project["id"],
                        title=project["title"],
                        subtitle=project["subtitle"],
                        description=project["description"],
                        tech=project["tech"],
                        metrics=project["metrics"],
                        github=project["github"],
                        demo=project["demo"],
                        status=project["status"],
                    )
                )

        if not Experience.query.first():
            for experience in defaults.EXPERIENCE:
                db.session.add(
                    Experience(
                        role=experience["role"],
                        company=experience["company"],
                        period=experience["period"],
                        location=experience["location"],
                        highlights=experience["highlights"],
                    )
                )

        if not User.query.filter_by(username="admin").first():
            admin_password = os.environ.get("ADMIN_PASSWORD", "admin123")
            user = User(username="admin", is_admin=True)
            user.set_password(admin_password)
            db.session.add(user)
            click.echo("Created admin user with username 'admin'.")

        db.session.commit()
        click.echo("Seeded default portfolio content.")


@app.cli.command("create-admin")
@click.argument("username")
@click.argument("password")
def create_admin(username, password):
    """Create a new admin user from the command line."""
    with app.app_context():
        if User.query.filter_by(username=username).first():
            click.echo("A user with that username already exists.")
            return
        user = User(username=username, is_admin=True)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        click.echo(f"Created admin user '{username}'.")
