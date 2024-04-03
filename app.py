import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
from dotenv import load_dotenv
import uuid

load_dotenv()  # os env (environmental variable)
print(os.environ.get("AZURE_DATABASE_URL"))  # , os.environ.get("FORM_SECRET_KEY")

app = Flask(__name__)
# app.config["SECRET_KEY"] = os.environ.get("FORM_SECRET_KEY")  # "my_secret_key"  # token

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


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.String(50), primary_key=True, default=lambda: str(uuid.uuid4()))
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(100))

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "password": self.password,
        }


try:
    with app.app_context():
        # Use text() to explicitly declare your SQL command
        result = db.session.execute(text("SELECT 1")).fetchall()
        print("Connection successful:", result)
        db.create_all()  # syncing
except Exception as e:
    print("Error connecting to the database:", e)


from about_bp import about_bp
from movies_bp import movies_bp
from movie_list_bp import movie_list_bp

# from login_bp import login_bp
from users_bp import users_bp
from main_bp import main_bp

app.register_blueprint(about_bp, url_prefix="/about")
app.register_blueprint(movies_bp, url_prefix="/movies")
app.register_blueprint(movie_list_bp, url_prefix="/movie-list")
# app.register_blueprint(login_bp, url_prefix="/login")
app.register_blueprint(users_bp)
app.register_blueprint(main_bp)


# if __name__ == "__main__":
#     app.run(debug=True)
