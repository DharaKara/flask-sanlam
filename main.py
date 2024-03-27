import os
from flask import Flask, jsonify, request, render_template, redirect, url_for
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
try:
    with app.app_context():
        # Use text() to explicitly declare your SQL command
        result = db.session.execute(text("SELECT 1")).fetchall()
        print("Connection successful:", result)
except Exception as e:
    print("Error connecting to the database:", e)


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


# /movies -> json
@app.get("/movies")
def get_movies():
    movie_list = Movie.query.all()  # select * from movies | movie_list iterator
    data = [movie.to_dict() for movie in movie_list]  # lisy of dictionaries
    return jsonify(data)


# task 1: data from azure (mySQL)
@app.get("/movies/<id>")
def get_movie(id):
    movie = Movie.query.get(id)
    if movie:
        return jsonify(movie.to_dict())
    else:
        return jsonify({"message": "Movie not found"}), 404


# task 2: /movies-list -> display the data on the page
@app.route("/movie-list")
def movie_list():
    movie_list = Movie.query.all()
    data = [movie.to_dict() for movie in movie_list]
    return render_template("movie-list.html", movies=data)


# task 3: /movies-list/99 -> display the data on the page from azure (mysql)
@app.route("/movie-list/<movie_id>")
def movie_detail(movie_id):
    movie = Movie.query.get(movie_id)
    data = movie.to_dict()
    if data:
        return render_template("movie-detail.html", movie=data)
    else:
        return "<h1>Movie not found</h1>", 404


# task 4: db.session.delete(movie)
@app.delete("/movies/<id>")
def delete_movie(id):
    # Permission to modify the lexical scope variable
    filtered_movie = Movie.query.get(id)
    if not filtered_movie:
        return jsonify({"message": "Movie not found"}), 404

    try:
        data = filtered_movie.to_dict()
        db.session.delete(filtered_movie)
        db.session.commit()  # Making the change (update/delete/create) permanent
        return jsonify({"message": "Deleted Successfully", "data": data})
    except Exception as e:
        db.session.rollback()  # Undo the change
        return jsonify({"message": str(e)}), 500


# task 5, add
# you cant undo after commit, so if error, rollback()
# @app.post("/movies")
# def create_movies():
#     data = request.json  # body
#     new_movie = Movie(
#         name=data["name"],
#         poster=data["poster"],
#         rating=data["rating"],
#         summary=data["summary"],
#         trailer=data["trailer"],
#     )
#     db.session.add(new_movie)
#     db.session.commit()
#     # movies.append(new_movie)
#     result = {"message": "Added Successfully", "data": new_movie.to_dict()}
#     return jsonify(result), 201


# task 6: exception handling
@app.post("/movies")
def create_movies():
    try:
        data = request.json
        new_movie = Movie(
            # **data
            name=data["name"],
            poster=data["poster"],
            rating=data["rating"],
            summary=data["summary"],
            trailer=data["trailer"],
        )
        db.session.add(new_movie)
        db.session.commit()
        result = {"message": "Added Successfully", "data": new_movie.to_dict()}
        return jsonify(result), 201
    except KeyError as e:
        error_message = f"KeyError: Missing required field '{e.args[0]}'"
        return jsonify({"message": error_message}), 400
    except Exception as e:
        db.session.rollback()  # Rollback changes if an error occurs
        return jsonify({"message": str(e)}), 500


# task 7: convert to db call
@app.put("/movies/<id>")
def update_movie_by_id(id):
    data = request.json
    movie_to_update = Movie.query.get(id)
    try:
        # movie_to_update.name = data.get("name", movie_to_update.name)
        # movie_to_update.poster = data.get("poster", movie_to_update.poster)
        # movie_to_update.rating = data.get("rating", movie_to_update.rating)
        # movie_to_update.summary = data.get("summary", movie_to_update.summary)
        # movie_to_update.trailer = data.get("trailer", movie_to_update.trailer)
        for key, value in data.items():
            if hasattr(movie_to_update, key, value):
                setattr(movie_to_update, key, value)
        db.session.commit()
        return jsonify({"message": "Movie updated", "data": movie_to_update.to_dict()})
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": str(e)}), 500


# local- not in db
# movies = [
#     {
#         "id": "99",
#         "name": "Vikram",
#         "poster": "https://m.media-amazon.com/images/M/MV5BMmJhYTYxMGEtNjQ5NS00MWZiLWEwN2ItYjJmMWE2YTU1YWYxXkEyXkFqcGdeQXVyMTEzNzg0Mjkx._V1_.jpg",
#         "rating": 8.4,
#         "summary": "Members of a black ops team must track and eliminate a gang of masked murderers.",
#         "trailer": "https://www.youtube.com/embed/OKBMCL-frPU",
#     },
#     {
#         "id": "100",
#         "name": "RRR",
#         "poster": "https://englishtribuneimages.blob.core.windows.net/gallary-content/2021/6/Desk/2021_6$largeimg_977224513.JPG",
#         "rating": 8.8,
#         "summary": "RRR is an upcoming Indian Telugu-language period action drama film directed by S. S. Rajamouli, and produced by D. V. V. Danayya of DVV Entertainments.",
#         "trailer": "https://www.youtube.com/embed/f_vbAtFSEc0",
#     },
#     {
#         "id": "101",
#         "name": "Iron man 2",
#         "poster": "https://m.media-amazon.com/images/M/MV5BMTM0MDgwNjMyMl5BMl5BanBnXkFtZTcwNTg3NzAzMw@@._V1_FMjpg_UX1000_.jpg",
#         "rating": 7,
#         "summary": "With the world now aware that he is Iron Man, billionaire inventor Tony Stark (Robert Downey Jr.) faces pressure from all sides to share his technology with the military. He is reluctant to divulge the secrets of his armored suit, fearing the information will fall into the wrong hands. With Pepper Potts (Gwyneth Paltrow) and Rhodes (Don Cheadle) by his side, Tony must forge new alliances and confront a powerful new enemy.",
#         "trailer": "https://www.youtube.com/embed/wKtcmiifycU",
#     },
#     {
#         "id": "102",
#         "name": "No Country for Old Men",
#         "poster": "https://upload.wikimedia.org/wikipedia/en/8/8b/No_Country_for_Old_Men_poster.jpg",
#         "rating": 8.1,
#         "summary": "A hunter's life takes a drastic turn when he discovers two million dollars while strolling through the aftermath of a drug deal. He is then pursued by a psychopathic killer who wants the money.",
#         "trailer": "https://www.youtube.com/embed/38A__WT3-o0",
#     },
#     {
#         "id": "103",
#         "name": "Jai Bhim",
#         "poster": "https://m.media-amazon.com/images/M/MV5BY2Y5ZWMwZDgtZDQxYy00Mjk0LThhY2YtMmU1MTRmMjVhMjRiXkEyXkFqcGdeQXVyMTI1NDEyNTM5._V1_FMjpg_UX1000_.jpg",
#         "summary": "A tribal woman and a righteous lawyer battle in court to unravel the mystery around the disappearance of her husband, who was picked up the police on a false case",
#         "rating": 8.8,
#         "trailer": "https://www.youtube.com/embed/nnXpbTFrqXA",
#     },
#     {
#         "id": "104",
#         "name": "The Avengers",
#         "rating": 8,
#         "summary": "Marvel's The Avengers (classified under the name Marvel Avengers\n Assemble in the United Kingdom and Ireland), or simply The Avengers, is\n a 2012 American superhero film based on the Marvel Comics superhero team\n of the same name.",
#         "poster": "https://terrigen-cdn-dev.marvel.com/content/prod/1x/avengersendgame_lob_crd_05.jpg",
#         "trailer": "https://www.youtube.com/embed/eOrNdBpGMv8",
#     },
#     {
#         "id": "105",
#         "name": "Interstellar",
#         "poster": "https://m.media-amazon.com/images/I/A1JVqNMI7UL._SL1500_.jpg",
#         "rating": 8.6,
#         "summary": "When Earth becomes uninhabitable in the future, a farmer and ex-NASA\n pilot, Joseph Cooper, is tasked to pilot a spacecraft, along with a team\n of researchers, to find a new planet for humans.",
#         "trailer": "https://www.youtube.com/embed/zSWdZVtXT7E",
#     },
#     {
#         "id": "106",
#         "name": "Baahubali",
#         "poster": "https://flxt.tmsimg.com/assets/p11546593_p_v10_af.jpg",
#         "rating": 8,
#         "summary": "In the kingdom of Mahishmati, Shivudu falls in love with a young warrior woman. While trying to woo her, he learns about the conflict-ridden past of his family and his true legacy.",
#         "trailer": "https://www.youtube.com/embed/sOEg_YZQsTI",
#     },
#     {
#         "id": "107",
#         "name": "Ratatouille",
#         "poster": "https://resizing.flixster.com/gL_JpWcD7sNHNYSwI1ff069Yyug=/ems.ZW1zLXByZC1hc3NldHMvbW92aWVzLzc4ZmJhZjZiLTEzNWMtNDIwOC1hYzU1LTgwZjE3ZjQzNTdiNy5qcGc=",
#         "rating": 8,
#         "summary": "Remy, a rat, aspires to become a renowned French chef. However, he fails to realise that people despise rodents and will never enjoy a meal cooked by him.",
#         "trailer": "https://www.youtube.com/embed/NgsQ8mVkN8w",
#     },
#     {
#         "name": "PS2",
#         "poster": "https://m.media-amazon.com/images/M/MV5BYjFjMTQzY2EtZjQ5MC00NGUyLWJiYWMtZDI3MTQ1MGU4OGY2XkEyXkFqcGdeQXVyNDExMjcyMzA@._V1_.jpg",
#         "summary": "Ponniyin Selvan: I is an upcoming Indian Tamil-language epic period action film directed by Mani Ratnam, who co-wrote it with Elango Kumaravel and B. Jeyamohan",
#         "rating": 8,
#         "trailer": "https://www.youtube.com/embed/KsH2LA8pCjo",
#         "id": "108",
#     },
#     {
#         "name": "Thor: Ragnarok",
#         "poster": "https://m.media-amazon.com/images/M/MV5BMjMyNDkzMzI1OF5BMl5BanBnXkFtZTgwODcxODg5MjI@._V1_.jpg",
#         "summary": "When Earth becomes uninhabitable in the future, a farmer and ex-NASA\\n pilot, Joseph Cooper, is tasked to pilot a spacecraft, along with a team\\n of researchers, to find a new planet for humans.",
#         "rating": 8.8,
#         "trailer": "https://youtu.be/NgsQ8mVkN8w",
#         "id": "109",
#     },
# ]


# @app.route("/")  # HOF
# def hello_world():
#     return "<h1>Hello, World! 🙂</h1>"


# @app.route("/about")  # HOF
# def about():
#     return "<h1>About page</h1>"


# if __name__ == "__main__":
#     app.run(debug=True)


# /movies -> json
# @app.get("/movies")
# def get_movies():
#     return jsonify(movies)


# <variable_name> | id --> Keyword argument
# @app.get("/movies/<id>")
# def get_movie(id):
#     return id


# task 1.1 - handle negative scenario
# my solution
# @app.get("/movies/<id>")
# def get_movie(id):
#     for movie in movies:
#         if movie["id"] == id:
#             return jsonify(movie)
#     return jsonify({"message": "Movie not found"}), 404


# ragavs solution
# @app.get("/movies/<id>")
# def get_movie(id):
#     # seniors will do it this way
#     # generator expression () | find an item list | instead of using list comp
#     filtered_movie = next((movie for movie in movies if movie["id"] == id), None)
#     return jsonify(filtered_movie)


# Task 1.1 - negative scenario with error
# @app.get("/movies/<id>")
# def get_movie(id):
#     filtered_movie = next((movie for movie in movies if movie["id"] == id), None)
#     if filtered_movie:
#         return jsonify(filtered_movie)
#     return jsonify({"message": "Movie not found"}), 404


# @app.post("/movies")
# def add_movie():
#     new_movie = request.json
#     movies.append(new_movie)
#     print(new_movie)
#     result = {"message": "Added successfully"}
#     return jsonify(result), 201


# task: create one more movie and send back the data, dont just assume id, use python skills.
# @app.post("/movies")
# def add_movie():
#     new_movie_data = request.json
#     max_id = max(
#         int(movie["id"]) for movie in movies
#     )  # looped through movies and converted it to int to find max id
#     new_id = str(max_id + 1)  # added 1 to the max id and then converted back to a str
#     new_movie_data["id"] = new_id
#     movies.append(new_movie_data)
#     print(new_movie_data)
#     return jsonify({"message": "Added successfully", "movie": new_movie_data}), 201


# Task - 2
# Create Delete API for movies
# @app.delete("/movies/<id>")
# def delete_movie(id):
#     filtered_movie = next((movie for movie in movies if movie["id"] == id), None)
#     movies.remove(filtered_movie)
#     return jsonify(filtered_movie)

# Task 2 -> ragavs way
# @app.delete("/movies/<id>")
# def delete_movie(id):
#     # permission to modify the lexical scope variable | reassign not allowed
#     global movies
#     movies = [movie for movie in movies if movie["id"] != id]
#     return jsonify({"message": "Movie deleted successfully"}), 200


# Task - 2.1 Negative scenario
# Create Delete API for movies
# @app.delete("/movies/<id>")
# def delete_movie(id):
#     # permission to modify the lexical scope
#     filtered_movie = next((movie for movie in movies if movie["id"] == id), None)
#     if filtered_movie:
#         movies.remove(filtered_movie)
#         return (
#             jsonify({"message": "Movie deleted successfully", "data": filtered_movie}),
#             200,
#         )
#     else:
#         return jsonify({"message": "Movie not found"}), 404


# # Update Movie
# @app.put("/movies/<id>")
# def update_movie(id):
#     # next doesnt create a copy like list comp, it will update original list
#     filtered_movie = next(
#         (movie for movie in movies if movie["id"] == id), None
#     )  # Find the movie with the given ID
#     if not filtered_movie:  # If movie is not found, return 404 Not Found response
#         return jsonify({"message": "Movie not found"}), 404
#     data = request.json  # Extract data from request JSON payload (from body)
#     # we are updating in place | unpack ** to make a copy
#     filtered_movie.update(data)  # Update the movie information with the provided data
#     return (
#         jsonify({"message": "Movie updated successfully", "movie": filtered_movie}),
#         200,
#     )  # Return success message along with the updated movie information


# another way to do it
# @app.put("/movies/<id>")
# def update_movie_by_id(id):
#     movie_idx = next((idx for idx, movie in enumerate(movies) if movie["id"] == id), None) # same memory
#     body = request.json
#     movies[movie_idx] = {**movies[movie_idx], **body}


@app.route("/")
def hello_world():
    return "<h1>Super, Cool 🙂</h1>"


# user = {
#     "name": "Dhara",
#     "pic": "https://i.pinimg.com/236x/db/b9/cb/dbb9cbe3b84da22c294f57cc7847977e.jpg",
# }

# users = [
#     {
#         "name": "Arjun",
#         "pic": "https://i.pinimg.com/236x/db/b9/cb/dbb9cbe3b84da22c294f57cc7847977e.jpg",
#     },
#     {
#         "name": "Monisha",
#         "pic": "https://i.pinimg.com/236x/db/b9/cb/dbb9cbe3b84da22c294f57cc7847977e.jpg",
#     },
#     {
#         "name": "Saravanan",
#         "pic": "https://i.pinimg.com/236x/db/b9/cb/dbb9cbe3b84da22c294f57cc7847977e.jpg",
#     },
# ]

# movies = [
#     {
#         "id": "99",
#         "name": "Vikram",
#         "poster": "https://m.media-amazon.com/images/M/MV5BMmJhYTYxMGEtNjQ5NS00MWZiLWEwN2ItYjJmMWE2YTU1YWYxXkEyXkFqcGdeQXVyMTEzNzg0Mjkx._V1_.jpg",
#         "rating": 8.4,
#         "summary": "Members of a black ops team must track and eliminate a gang of masked murderers.",
#         "trailer": "https://www.youtube.com/embed/OKBMCL-frPU",
#     },
#     {
#         "id": "100",
#         "name": "RRR",
#         "poster": "https://englishtribuneimages.blob.core.windows.net/gallary-content/2021/6/Desk/2021_6$largeimg_977224513.JPG",
#         "rating": 8.8,
#         "summary": "RRR is an upcoming Indian Telugu-language period action drama film directed by S. S. Rajamouli, and produced by D. V. V. Danayya of DVV Entertainments.",
#         "trailer": "https://www.youtube.com/embed/f_vbAtFSEc0",
#     },
#     {
#         "id": "101",
#         "name": "Iron man 2",
#         "poster": "https://m.media-amazon.com/images/M/MV5BMTM0MDgwNjMyMl5BMl5BanBnXkFtZTcwNTg3NzAzMw@@._V1_FMjpg_UX1000_.jpg",
#         "rating": 7,
#         "summary": "With the world now aware that he is Iron Man, billionaire inventor Tony Stark (Robert Downey Jr.) faces pressure from all sides to share his technology with the military. He is reluctant to divulge the secrets of his armored suit, fearing the information will fall into the wrong hands. With Pepper Potts (Gwyneth Paltrow) and Rhodes (Don Cheadle) by his side, Tony must forge new alliances and confront a powerful new enemy.",
#         "trailer": "https://www.youtube.com/embed/wKtcmiifycU",
#     },
#     {
#         "id": "102",
#         "name": "No Country for Old Men",
#         "poster": "https://upload.wikimedia.org/wikipedia/en/8/8b/No_Country_for_Old_Men_poster.jpg",
#         "rating": 8.1,
#         "summary": "A hunter's life takes a drastic turn when he discovers two million dollars while strolling through the aftermath of a drug deal. He is then pursued by a psychopathic killer who wants the money.",
#         "trailer": "https://www.youtube.com/embed/38A__WT3-o0",
#     },
#     {
#         "id": "103",
#         "name": "Jai Bhim",
#         "poster": "https://m.media-amazon.com/images/M/MV5BY2Y5ZWMwZDgtZDQxYy00Mjk0LThhY2YtMmU1MTRmMjVhMjRiXkEyXkFqcGdeQXVyMTI1NDEyNTM5._V1_FMjpg_UX1000_.jpg",
#         "summary": "A tribal woman and a righteous lawyer battle in court to unravel the mystery around the disappearance of her husband, who was picked up the police on a false case",
#         "rating": 8.8,
#         "trailer": "https://www.youtube.com/embed/nnXpbTFrqXA",
#     },
#     {
#         "id": "104",
#         "name": "The Avengers",
#         "rating": 8,
#         "summary": "Marvel's The Avengers (classified under the name Marvel Avengers\n Assemble in the United Kingdom and Ireland), or simply The Avengers, is\n a 2012 American superhero film based on the Marvel Comics superhero team\n of the same name.",
#         "poster": "https://terrigen-cdn-dev.marvel.com/content/prod/1x/avengersendgame_lob_crd_05.jpg",
#         "trailer": "https://www.youtube.com/embed/eOrNdBpGMv8",
#     },
#     {
#         "id": "105",
#         "name": "Interstellar",
#         "poster": "https://m.media-amazon.com/images/I/A1JVqNMI7UL._SL1500_.jpg",
#         "rating": 8.6,
#         "summary": "When Earth becomes uninhabitable in the future, a farmer and ex-NASA\n pilot, Joseph Cooper, is tasked to pilot a spacecraft, along with a team\n of researchers, to find a new planet for humans.",
#         "trailer": "https://www.youtube.com/embed/zSWdZVtXT7E",
#     },
#     {
#         "id": "106",
#         "name": "Baahubali",
#         "poster": "https://flxt.tmsimg.com/assets/p11546593_p_v10_af.jpg",
#         "rating": 8,
#         "summary": "In the kingdom of Mahishmati, Shivudu falls in love with a young warrior woman. While trying to woo her, he learns about the conflict-ridden past of his family and his true legacy.",
#         "trailer": "https://www.youtube.com/embed/sOEg_YZQsTI",
#     },
#     {
#         "id": "107",
#         "name": "Ratatouille",
#         "poster": "https://resizing.flixster.com/gL_JpWcD7sNHNYSwI1ff069Yyug=/ems.ZW1zLXByZC1hc3NldHMvbW92aWVzLzc4ZmJhZjZiLTEzNWMtNDIwOC1hYzU1LTgwZjE3ZjQzNTdiNy5qcGc=",
#         "rating": 8,
#         "summary": "Remy, a rat, aspires to become a renowned French chef. However, he fails to realise that people despise rodents and will never enjoy a meal cooked by him.",
#         "trailer": "https://www.youtube.com/embed/NgsQ8mVkN8w",
#     },
#     {
#         "name": "PS2",
#         "poster": "https://m.media-amazon.com/images/M/MV5BYjFjMTQzY2EtZjQ5MC00NGUyLWJiYWMtZDI3MTQ1MGU4OGY2XkEyXkFqcGdeQXVyNDExMjcyMzA@._V1_.jpg",
#         "summary": "Ponniyin Selvan: I is an upcoming Indian Tamil-language epic period action film directed by Mani Ratnam, who co-wrote it with Elango Kumaravel and B. Jeyamohan",
#         "rating": 8,
#         "trailer": "https://www.youtube.com/embed/KsH2LA8pCjo",
#         "id": "108",
#     },
#     {
#         "name": "Thor: Ragnarok",
#         "poster": "https://m.media-amazon.com/images/M/MV5BMjMyNDkzMzI1OF5BMl5BanBnXkFtZTgwODcxODg5MjI@._V1_.jpg",
#         "summary": "When Earth becomes uninhabitable in the future, a farmer and ex-NASA\\n pilot, Joseph Cooper, is tasked to pilot a spacecraft, along with a team\\n of researchers, to find a new planet for humans.",
#         "rating": 8.8,
#         "trailer": "https://youtu.be/NgsQ8mVkN8w",
#         "id": "109",
#     },
# ]


# @app.route("/movie-list")
# def movie_list_page():
#     return render_template("movie-list.html", movies=movies)


# @app.route("/movie-list/<movie_id>")
# def movie_detail(movie_id):
#     movie = next((movie for movie in movies if movie["id"] == movie_id), None)
#     if movie:
#         return render_template("movie-detail.html", movie=movie)
#     else:
#         return "<h1>Movie not found</h1>", 404


# @app.route("/about")
# def about_page():
#     return render_template("about.html", movies=movies)


name = "Caleb"
hobbies = ["Gaming", "Reading", "Soccer", "Ballet", "Gyming"]


@app.route("/profile")
def profile_page():
    return render_template("profile.html", name=name, hobbies=hobbies)


@app.route("/login", methods=["GET"])
def login_page():
    return render_template("forms.html")


@app.route("/dashboard", methods=["POST"])
def dashboard_page():
    username = request.form.get("username")
    password = request.form.get("password")
    print("Dashboard page", username, password)
    return f"<h1>Hi, {username}</h1>"


# not secure but you can use it for search functionality
# @app.route("/dashboard", methods=["GET"])
# def dashboard_page():
#     username = request.args.get("username")
#     password = request.args.get("password")
#     print("Dashboard page", username, password)
#     return f"<h1>Hi, {username}</h1>"


# ================


@app.route("/movie-list/add", methods=["POST"])
def added_movie():
    data = {
        "name": request.form.get("name"),
        "poster": request.form.get("poster"),
        "rating": float(request.form.get("rating")),  # Convert rating to float
        "summary": request.form.get("summary"),
        "trailer": request.form.get("trailer")
    }
    try:
        new_movie = Movie(**data)
        db.session.add(new_movie)
        db.session.commit()
        return f"<h1>{data["name"]} added Successfully</h1>"
    except Exception as e:
        db.session.rollback()
        return f"<h1>Error occurred: {str(e)}</h1>", 500
    
def delete_movie_by_id():
    print(request.form.get("movie_id"))
    id = request.form.get("movie_id")
    filtered_movie = Movie.query.get(id)
    if not filtered_movie:
        return "<h1>Movie not found</h1>", 404
    try:
        data = filtered_movie.to_dict()
        db.session.delete(filtered_movie)
        db.session.commit()  # Making the change (update/delete/create) permanent
        return f"<h1>{data['name']} Movie deleted Successfully</h1>"
    except Exception as e:
        db.session.rollback()  # Undo the change
        return f"<h1>Error happened {str(e)}</h1>", 500


@app.route("/movie-list/delete", methods=["POST"])  # HOF
def delete_movie_by_id():
    print(request.form.get("movie_id"))
    id = request.form.get("movie_id")
    filtered_movie = Movie.query.get(id)
    if not filtered_movie:
        return "<h1>Movie not found</h1>", 404
    try:
        data = filtered_movie.to_dict()
        db.session.delete(filtered_movie)
        db.session.commit()  # Making the change (update/delete/create) permanent
        return f"<h1>{data['name']} Movie deleted Successfully</h1>"
    except Exception as e:
        db.session.rollback()  # Undo the change
        return f"<h1>Error happened {str(e)}</h1>", 500


# @app.route("/movie-list/success", methods=["POST"])  # HOF
# def create_movie():
#     name = request.form.get("name")
#     poster = request.form.get("poster")
#     rating = request.form.get("rating")
#     summary = request.form.get("summary")
#     trailer = request.form.get("trailer")
#     print(name, poster, rating, summary, trailer)

#     # Creating a dictionary
#     new_movie = {
#         "name": name,
#         "poster": poster,
#         "rating": rating,
#         "summary": summary,
#         "trailer": trailer,
#     }

#     # Creating the new id
#     movie_ids = [int(movie["id"]) for movie in movies]
#     max_id = max(movie_ids)
#     new_movie["id"] = str(max_id + 1)
#     # adding the to the list
#     movies.append(new_movie)

#     return "<h1>Movie added Successfully</h1>"


if __name__ == "__main__":
    app.run(debug=True)
