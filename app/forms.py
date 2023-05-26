from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired
from wtforms import StringField, TextAreaField, FileField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length


class ReviewForm(FlaskForm):
    name = StringField("Имя", validators=[
        DataRequired(message='Поля "Имя" не может быть пустым'),
        Length(max=255, message="Имя не может быть длинее 255 символов")
    ])
    review = TextAreaField("Отзыв", validators=[
        DataRequired(message='Поля "Отзыв" не может быть пустым')
    ])
    rating = SelectField("Оценка", choices=range(1, 11))
    submit = SubmitField("Оставить отзыв")


class MovieForm(FlaskForm):
    title = StringField("Название", validators=[
        DataRequired(message='Поля "Название" не может быть пустым'),
        Length(max=255, message="Название не может быть длинее 255 символов")
    ])
    description = TextAreaField("Описание", validators=[
        DataRequired(message='Поля "Описание" не может быть пустым')
    ])
    image = FileField("Постер", validators=[
        FileRequired(message="Фильм не может быть добавлен без постера")
    ])
    submit = SubmitField("Добавить фильм")
