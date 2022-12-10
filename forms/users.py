from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, SubmitField, RadioField, DateField
from wtforms import BooleanField, StringField, IntegerField, SelectField
from wtforms.validators import DataRequired, EqualTo, Length, ValidationError


class RegisterForm(FlaskForm):
    """Форма для 1 шага регистрации"""
    username = StringField('Логин',
                           validators=[DataRequired(), Length(min=3, message='В логие должно быть минимум 3 символа!')])
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль',
                             validators=[DataRequired(), EqualTo('password_again', message='Пароли не совпадают!')])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired()])
    tip = RadioField(choices=['СТУДЕНТ', 'КОМПАНИЯ'], default='СТУДЕНТ')
    submit = SubmitField('ДАЛЕЕ')

    def validate_username(self, username):
        excluded_chars = " *?!'^+%&;/()=}][{$#"
        for char in self.username.data:
            if char in excluded_chars:
                raise ValidationError(
                    f"Character {char} is not allowed in username.")


class StudentRegisterForm(FlaskForm):
    """Форма для 2 шага регистрации (студент)"""
    name = StringField('Имя', validators=[DataRequired(), Length(min=2, message='Слишком короткое имя!')])
    surname = StringField('Фамилия', validators=[DataRequired(), Length(min=2, message='Слишком короткая фамилия!')])
    birthday = DateField(format='%d.%m.%Y')
    study_place = StringField('Учебное заведение',
                              validators=[DataRequired(),
                                          Length(min=2, message='Такого учебного заведения не существует!!')])
    program = StringField('Направление',
                          validators=[DataRequired(), Length(min=2, message='Такого направления не существует!')])
    grade = SelectField('Степень обучения: ',
                        choices=[(x, x) for x in ['Бакалавр', 'Магистр', 'Специалист', 'Аспирант', 'Выпускник']],
                        default='Бакалавр')
    course = IntegerField('Курс', validators=[DataRequired()], default=1)
    submit = SubmitField('ДАЛЕЕ')


class LoginForm(FlaskForm):
    """Форма для авторизации"""
    email = EmailField('Логин/Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('ВОЙТИ')


# class EditUserForm(FlaskForm):
#     """Форма для редактирования пользователя"""
#     username = StringField('Логин', validators=[DataRequired()])
#     name = StringField('Имя', validators=[DataRequired()])
#     surname = StringField('Фамилия', validators=[DataRequired()])
#     age = IntegerField('Возраст')
#     about = TextAreaField("Немного о себе")
#     submit = SubmitField('Внести изменения')
