from flask import Blueprint, render_template

# from app import db, Movie
from extensions import db

# from folder.filename import model
from models.users import User

users_bp = Blueprint("users_bp", __name__)
# Task - User Model | id, username, password
# Sign Up page
# Login page

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, ValidationError
from wtforms.validators import InputRequired, Length

# register page


class RegistrationForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired(), Length(min=6)])
    password = PasswordField(
        "Password", validators=[InputRequired(), Length(min=8, max=12)]
    )
    submit = SubmitField("Sign Up")

    # def validate_<fieldname>
    # validate_username() called form.validate_on_submit()
    def validate_username(self, field):
        # inform WTF that there is an error
        user_from_db = User.query.filter_by(username=field.data).first()
        if user_from_db:
            raise ValidationError("Username is taken")


# ==========================================================================

# version 1

# @app.route("/register", methods=["GET", "POST"])  # HOF
# def register_page():
#     form = RegistrationForm()  # get a post
#     if form.validate_on_submit():  # only on post
#         print(
#             form.username.data, form.password.data
#         )  # task: add this data to your db (create model, pass the data call submit)
#         return "<h1>Registration successful</h1>"
#     return render_template("register.html", form=form)  # only get


# get = issue token
# post - verify token

# ==========================================================================

# version 2

# @app.route("/register", methods=["GET", "POST"])
# def register_page():
#     form = RegistrationForm()
#     data = {"username": form.username.data, "password": form.password.data}
#     all_users = User.query.all()
#     ans = [user.to_dict() for user in all_users]
#     found_user = next(
#         (user for user in ans if (user["username"] == data["username"])),
#         None,
#     )
#     if form.validate_on_submit():
#         if found_user:
#             return "<h2>Username already exists</h2>"
#         new_user = User(**data)

#         try:
#             db.session.add(new_user)
#             db.session.commit()
#             return f"<h2>{data['username']} has been registered</h2>"
#         except Exception as e:
#             db.session.rollback()
#             return "<h2>Error Occurred</h2>"

#     return render_template("registration.html", form=form)

# ==========================================================================


# db post
@users_bp.route("/register", methods=["GET", "POST"])
def register_page():
    form = RegistrationForm()
    if form.validate_on_submit():
        new_user = User(username=form.username.data, password=form.password.data)
        try:
            db.session.add(new_user)
            db.session.commit()
            return "<h2>User has been registered</h2>", 201
        except Exception as e:
            db.session.rollback()
            return f"<h2>Error happened {str(e)}</h2>", 500
    return render_template("register.html", form=form)


# ==========================================================================


# login page
class LoginForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired(), Length(min=6)])
    password = PasswordField(
        "Password", validators=[InputRequired(), Length(min=8, max=12)]
    )
    submit = SubmitField("Log In")

    def validate_username(self, field):
        user_from_db = User.query.filter_by(username=field.data).first()
        if not user_from_db:
            raise ValidationError("Invalid username")

    def validate_password(self, field):
        user_from_db = User.query.filter_by(username=self.username.data).first()
        if user_from_db:
            form_password = field.data
            user_db_data = user_from_db.to_dict()
            print(user_db_data, form_password)
            if user_db_data["password"] != form_password:
                raise ValidationError("Invalid password")


@users_bp.route("/login", methods=["GET", "POST"])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        return "<h2>Logged in successfully</h2>", 200
    return render_template("login.html", form=form)
