from flask import Blueprint, render_template, request, redirect, url_for
from main import db, Movie

movie_list_bp = Blueprint("movie_list_bp", __name__)


# Task 2: /movies-list -> Display the data on the page from Azure (MSSQL)
# Movie list dashboard
@movie_list_bp.route("/")  # HOF
def movie_list_page():
    movie_list = Movie.query.all()  # Select * from movies | movie_list iterator
    data = [movie.to_dict() for movie in movie_list]  # list of dictionaries
    return render_template("movie-list.html", movies=data)


# Task 3: /movies-list/99 -> Display the data on the page from Azure (MSSQL)
# Movie list detail
@movie_list_bp.route("/<id>")  # HOF
def movie_detail_page(id):
    filtered_movie = Movie.query.get(id)
    if filtered_movie:
        data = filtered_movie.to_dict()
        return render_template("movie-detail.html", movie=data)
    else:
        return "<h1>Movie not found</h1>"


@movie_list_bp.route("/add", methods=["GET"])  # HOF
def add_movie():
    return render_template("add-movie.html")


@movie_list_bp.route("/delete", methods=["POST"])  # HOF
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


@movie_list_bp.route("/success", methods=["POST"])  # HOF
def create_movie():
    # Creating a dictionary
    data = {
        "name": request.form.get("name"),
        "poster": request.form.get("poster"),
        "rating": request.form.get("rating"),
        "summary": request.form.get("summary"),
        "trailer": request.form.get("trailer"),
    }

    new_movie = Movie(**data)
    try:
        db.session.add(new_movie)
        db.session.commit()
        # movies.append(new_movie)
        return f"<h1>{data['name']} Movie added Successfully</h1>"
    except Exception as e:
        db.session.rollback()  # Undo the change
        return f"<h1>Error happened {str(e)}</h1>", 500


# edit by id task
@movie_list_bp.route("/<id>", methods=["POST"])
def edit_movie_by_id(id):
    movie_id = request.form.get("movie_id")
    filtered_movie = Movie.query.get(movie_id)
    if not filtered_movie:
        return "<h1>Movie not found</h1>", 404

    name = request.form.get("name", filtered_movie.name)
    poster = request.form.get("poster", filtered_movie.poster)
    rating = request.form.get("rating", filtered_movie.rating)
    summary = request.form.get("summary", filtered_movie.summary)
    trailer = request.form.get("trailer", filtered_movie.trailer)

    try:
        filtered_movie.name = name
        filtered_movie.poster = poster
        filtered_movie.rating = rating
        filtered_movie.summary = summary
        filtered_movie.trailer = trailer

        db.session.commit()
        return redirect(url_for("movie_list_bp.edit-movie", id=movie_id))
    except Exception as e:
        db.session.rollback()
        return f"<h1>Error happened: {str(e)}</h1>", 500
