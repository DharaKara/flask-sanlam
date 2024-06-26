import os
from flask import Flask
from sqlalchemy.sql import text
from dotenv import load_dotenv
from extensions import db
from models.users import User
from flask_login import LoginManager


login_manager = LoginManager()

load_dotenv()  # os env (environmental variable)
print(os.environ.get("AZURE_DATABASE_URL"), os.environ.get("FORM_SECRET_KEY"))

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("FORM_SECRET_KEY")  # "my_secret_key"  # token

# mssql+pyodbc://<username>:<password>@<dsn_name>?driver=<driver_name>
# mssql+pyodbc://@<server_name>/<db_name>?driver=<driver_name>

connection_string = os.environ.get("AZURE_DATABASE_URL")
app.config["SQLALCHEMY_DATABASE_URI"] = connection_string

# db = SQLAlchemy(app)  # orm
db.init_app(app)
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    # Query your User model to retrieve the user based on the user_id
    return User.query.get(user_id)


try:
    with app.app_context():
        # Use text() to explicitly declare your SQL command
        result = db.session.execute(text("SELECT 1")).fetchall()
        print("Connection successful:", result)
        # db.drop_all()  # if table exists and you add columns it will not recreate, so we drop it to create it
        db.create_all()  # syncing
        print("Creation Done")
except Exception as e:
    print("Error connecting to the database:", e)


from routes.about_bp import about_bp
from routes.movies_bp import movies_bp
from routes.movie_list_bp import movie_list_bp
from routes.users_bp import users_bp
from routes.main_bp import main_bp

# from login_bp import login_bp

app.register_blueprint(about_bp, url_prefix="/about")
app.register_blueprint(movies_bp, url_prefix="/movies")
app.register_blueprint(movie_list_bp, url_prefix="/movie-list")
app.register_blueprint(users_bp)
app.register_blueprint(main_bp)

# app.register_blueprint(login_bp, url_prefix="/login")


# if __name__ == "__main__":
#     app.run(debug=True)
