from flask import Blueprint, render_template

login_bp = Blueprint("login_bp", __name__)


@login_bp.route("/login", methods=["GET"])
def login_page():
    return render_template("forms.html")
