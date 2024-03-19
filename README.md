https://flask.palletsprojects.com/en/3.0.x/quickstart/
https://flask.palletsprojects.com/en/3.0.x/installation/

python -m venv myenv
.\myenv\Scripts\Activate.ps1

git add .
git commit -m "Your commit message here"
git push origin master

pip install flask

flask --app main run
ctrl + C <-to exit>

shortcut:
flask run

development mode:
flask run --debug
