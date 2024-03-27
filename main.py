import os
from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
from dotenv import load_dotenv
import uuid

load_dotenv()  # os env (environmental variable)
print(os.environ.get("AZURE_DATABASE_URL"))

app = Flask(__name__)

# mssql+pyodbc://<username>:<password>@<dsn_name>?driver=<driver_name>
connection_string = os.environ.get("AZURE_DATABASE_URL")
app.config["SQLALCHEMY_DATABASE_URI"] = connection_string

db = SQLAlchemy(app)  # orm


class Movie(db.Model):
    __tablename__ = "movies"
    id = db.Column(db.String(50), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(100))
    poster = db.Column(db.String(255))
    rating = db.Column(db.Float)
    summary = db.Column(db.String(500))
    trailer = db.Column(db.String(255))

    # JSON - keys
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "poster": self.poster,
            "rating": self.rating,
            "description": self.summary,  # name it anything you want on how to display in frontend
            "trailer": self.trailer,
        }


try:
    with app.app_context():
        # Use text() to explicitly declare your SQL command
        result = db.session.execute(text("SELECT 1")).fetchall()
        print("Connection successful:", result)
except Exception as e:
    print("Error connecting to the database:", e)


from about_bp import about_bp
from movies_bp import movies_bp
from movie_list_bp import movie_list_bp
from login_bp import login_bp

app.register_blueprint(about_bp, url_prefix="/about")
app.register_blueprint(movies_bp, url_prefix="/movies")
app.register_blueprint(movie_list_bp, url_prefix="/movie-list")
app.register_blueprint(login_bp, url_prefix="/login")


name = "Caleb"
hobbies = ["Gaming", "Reading", "Soccer", "Ballet", "Gyming"]


@app.route("/profile")
def profile_page():
    return render_template("profile.html", name=name, hobbies=hobbies)


@app.route("/dashboard", methods=["POST"])
def dashboard_page():
    username = request.form.get("username")
    password = request.form.get("password")
    print("Dashboard page", username, password)
    return f"<h1>Hi, {username}</h1>"


# Task - User Model | id, username, password
# Sign Up page
# Login page

if __name__ == "__main__":
    app.run(debug=True)
