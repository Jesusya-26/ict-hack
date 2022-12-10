from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, SubmitField, RadioField, widgets, BooleanField
from wtforms.validators import DataRequired


class RegisterFormStep1(FlaskForm):
    """Форма для регистрации пользователя"""
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired()])
    string_of_files = ['Студент\r\nКомпания\r\n']
    type = RadioField('Кто Вы?', choices=[(x, x) for x in string_of_files[0].split()])
    submit = SubmitField('Дальше')


class LoginForm(FlaskForm):
    """Форма для авторизации"""
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


# class EditUserForm(FlaskForm):
#     """Форма для редактирования пользователя"""
#     username = StringField('Логин', validators=[DataRequired()])
#     name = StringField('Имя', validators=[DataRequired()])
#     surname = StringField('Фамилия', validators=[DataRequired()])
#     age = IntegerField('Возраст')
#     about = TextAreaField("Немного о себе")
#     submit = SubmitField('Внести изменения')
