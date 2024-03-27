from flask import jsonify, request, Blueprint
from main import Movie, db


movies_bp = Blueprint("movies", __name__)


@movies_bp.get("/")
def get_movies():
    movie_list = Movie.query.all()  # Select * from movies | movie_list iterator
    data = [movie.to_dict() for movie in movie_list]  # list of dictionaries
    return jsonify(data)


# Task 1: Data from Azure (MSSQL)
# Clue: .all() - .get()
@movies_bp.get("/<id>")
def get_movie(id):
    filtered_movie = Movie.query.get(id)
    if filtered_movie:
        data = filtered_movie.to_dict()
        return jsonify(data)
    else:
        return jsonify({"message": "Movie not found"}), 404


# Task 4 | db.session.delete(movie)
@movies_bp.delete("/<id>")
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


# Handle the error scenario
@movies_bp.post("/")
def create_movies():
    data = request.json  # body
    new_movie = Movie(**data)
    try:
        db.session.add(new_movie)
        db.session.commit()
        # movies.append(new_movie)
        result = {"message": "Added successfully", "data": new_movie.to_dict()}
        return jsonify(result), 201
    except Exception as e:
        db.session.rollback()  # Undo the change
        return jsonify({"message": str(e)}), 500


# Task: convert to DB call
@movies_bp.put("/<id>")
def update_movie_by_id(id):
    filtered_movie = Movie.query.get(id)
    if not filtered_movie:
        return jsonify({"message": "Movie not found"}), 404
    body = request.json  # user

    # body - {"rating": 4}
    try:
        for key, value in body.items():
            if hasattr(filtered_movie, key):
                setattr(filtered_movie, key, value)

        db.session.commit()
        return jsonify(
            {"message": "Movie updated successfully!", "data": filtered_movie.to_dict()}
        )
    except Exception as e:
        db.session.rollback()  # Undo the change
        return jsonify({"message": str(e)}), 500
