from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, SubmitField, RadioField, FormField, DateField
from wtforms import BooleanField, StringField, IntegerField, SelectField, FieldList
from wtforms.validators import DataRequired, EqualTo, Length


class RegisterForm(FlaskForm):
    """Форма для 1 шага регистрации"""
    username = StringField('Логин',
                           validators=[DataRequired(), Length(min=3, message='В логие должно быть минимум 3 символа!')])
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль',
                             validators=[DataRequired(), EqualTo('password_again', message='Пароли не совпадают!')])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired()])
    type = RadioField(choices=['СТУДЕНТ', 'КОМПАНИЯ'], default='СТУДЕНТ')
    submit = SubmitField('ДАЛЕЕ')


class EducationForm(FlaskForm):
    study_place = StringField('Учебное заведение',
                              validators=[DataRequired(), Length(min=3, message='Такого ВУЗа не существует!')])
    program = StringField('Направление',
                          validators=[DataRequired(), Length(min=3, message='Такого направления не существует!')])
    string_of_files = ['Бакалавр\r\nМагистр\r\nСпециалист\r\nАспирант\r\nВыпускник\r\n']
    grade = SelectField('Степень обучения: ', choices=[(x, x) for x in string_of_files[0].split()], default='Бакалавр')
    course = IntegerField(
        validators=[DataRequired(), Length(min=1, max=6, message="Некорректное значение")], default=1)


class StudentRegisterForm(FlaskForm):
    """Форма для 2 шага регистрации (студент)"""
    name = StringField('Имя', validators=[DataRequired(), Length(min=2, message='Слишком короткое имя!')])
    surname = StringField('Фамилия', validators=[DataRequired(), Length(min=2, message='Слишком короткая фамилия!')])
    birthday = DateField(validators=[DataRequired()], format='%d.%m.%Y')
    education = FieldList(FormField(EducationForm))
    submit = SubmitField('ДАЛЕЕ')


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
