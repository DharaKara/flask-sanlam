from flask import render_template, request, Blueprint

main_bp = Blueprint("main_bp", __name__)

name = "Caleb"
hobbies = ["Gaming", "Reading", "Soccer", "Ballet", "Gyming"]


@main_bp.route("/")
def hello_world():
    return "<h1>Hello, Sanlam! 😀</h1>"


@main_bp.route("/profile")
def profile_page():
    return render_template("profile.html", name=name, hobbies=hobbies)


@main_bp.route("/sample")
def sample():
    return render_template("sample.html")


@main_bp.route("/dashboard", methods=["POST"])
def dashboard_page():
    username = request.form.get("username")
    password = request.form.get("password")
    print("Dashboard page", username, password)
    return f"<h1>Hi, {username}</h1>"
