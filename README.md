https://flask.palletsprojects.com/en/3.0.x/quickstart/
https://flask.palletsprojects.com/en/3.0.x/installation/

python -m venv myenv
.\myenv\Scripts\Activate.ps1

git add .
git commit -m "Your commit message here"
git push origin master

pip install flask

flask --app main run --debug
ctrl + C <-to exit>

shortcut:
flask run

development mode:
flask run --debug

take snapshot of packages
pip freeze > requirements.txt
pip install -r requirements.txt

databases
pip install pyodbc
pip install SQLAlchemy

mssql+pyodbc://<username>:<password>@<dsn_name>?driver=<driver_name>

pip install python-dotenv
from dotenv load dotenv

pip install Flask-WTF