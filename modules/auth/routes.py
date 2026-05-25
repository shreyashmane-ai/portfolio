from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_user, logout_user
from ..models import User
from ..forms import LoginForm
from ..extensions import db

bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash("Signed in.", "success")
            return redirect(url_for("admin.index"))
        flash("Invalid credentials.", "danger")
    return render_template("admin/login.html", form=form)


@bp.route("/logout")
def logout():
    logout_user()
    flash("Signed out.", "success")
    return redirect(url_for("main.index"))
