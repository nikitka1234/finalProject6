from flask import render_template, redirect, url_for

from . import app, db
from .models import Review, Movie
from .forms import ReviewForm, MovieForm

from pathlib import Path
from werkzeug.utils import secure_filename


BASEDIR = Path(__file__).parent
UPLOAD_FOLDER = BASEDIR / "static" / "images"


def index():
    movies = Movie.query.order_by(Movie.id.desc()).all()

    return render_template("index.html", movies=movies)


def movie(id):
    movie_from_id = Movie.query.get(id)
    form = ReviewForm()

    if movie_from_id.review:
        avg_rating = round(sum([r.rating for r in movie_from_id.review]) / len(movie_from_id.review), 1)
    else:
        avg_rating = "оценок нет!"

    if form.validate_on_submit():
        review_model = Review()

        review_model.author = form.name.data
        review_model.review = form.review.data
        review_model.rating = form.rating.data
        review_model.movie_id = id

        db.session.add(review_model)
        db.session.commit()

        return redirect(url_for("movie", id=id))

    return render_template("movie.html", movie=movie_from_id, avg_rating=avg_rating, form=form)


def add_movie():
    form = MovieForm()

    if form.validate_on_submit():
        movie_model = Movie()

        movie_model.title = form.title.data
        movie_model.description = form.description.data

        image = form.image.data
        image_name = secure_filename(image.filename)
        UPLOAD_FOLDER.mkdir(exist_ok=True)
        image.save(UPLOAD_FOLDER / image_name)

        movie_model.image = image_name

        db.session.add(movie_model)
        db.session.commit()

        return redirect(url_for("index"))

    return render_template("add_movie.html", form=form)


def reviews():
    reviews_list = Review.query.order_by(Review.date.desc()).all()

    return render_template("reviews.html", reviews=reviews_list)


def delete_review(id):
    review = Review.query.get(id)

    if review:
        db.session.delete(review)
        db.session.commit()

        return redirect(url_for("reviews"))


app.add_url_rule("/", "index", index)
app.add_url_rule("/movie/<int:id>", "movie", movie, methods=["GET", "POST"])
app.add_url_rule("/add_movie", "add_movie", add_movie, methods=["GET", "POST"])
app.add_url_rule("/reviews", "reviews", reviews)
app.add_url_rule("/delete_review/<int:id>", "delete_review", delete_review)
