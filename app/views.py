from flask import render_template, redirect, url_for

from . import app, db
from .models import Review, Movie
# from .form import ReviewForm, MovieForm


def index():
    movies = Movie.query.order_by(Movie.id.desc()).all()

    return render_template("index.html", movies=movies)


def movie(id):
    movie_from_id = Movie.query.get(id)

    if movie_from_id.review:
        avg_rating = round(sum([r.rating for r in movie_from_id.review]) / len(movie_from_id.review), 1)
    else:
        avg_rating = "оценок нет!"

    return render_template("movie.html", movie=movie_from_id, avg_rating=avg_rating)


def add_movie():
    return "Добавить фильм"


def reviews():
    return "Отзывы"


def delete_review(id):
    return "Удалить отзыв"


app.add_url_rule("/", "index", index)
app.add_url_rule("/movie/<int:id>", "movie", movie, methods=["GET", "POST"])
app.add_url_rule("/add_movie", "add_movie", add_movie, methods=["GET", "POST"])
app.add_url_rule("/reviews", "reviews", reviews)
app.add_url_rule("/delete_review/<int:id>", "delete_review", delete_review)
