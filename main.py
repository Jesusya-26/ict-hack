import os
from flask import Flask, render_template, redirect, make_response, jsonify, request, abort, url_for
from flask_avatars import Avatars
from flask_login import LoginManager, login_required, logout_user, login_user
from flask_restful import Api
from data import db_session
from data.students import Student
from data.student_projects import StudentProject
from data.companies import Company
from data.company_projects import CompanyProject
from forms.users import RegisterForm, LoginForm, StudentRegisterForm
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ict_hackaton'
app.config['STUDENT_PHOTO_FOLDER'] = 'img/student_photos/'
app.config['COMPANY_PHOTO_FOLDER'] = 'img/company_photos/'
app.config['STUDENT_PROJECT_PHOTO_FOLDER'] = 'img/student_project_photos/'
app.config['COMPANY_PROJECT_PHOTO_FOLDER'] = 'img/company_project_photos/'
login_manager = LoginManager()
login_manager.init_app(app)
api = Api(app)
avatars = Avatars(app)  # для удобной работы с аватарками


def main():
    """Запуск приложения"""
    db_session.global_init("db/ict_hackaton.db")
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)


@login_manager.user_loader
def load_user(user_id):
    """Загрузка текущего пользователя"""
    db_sess = db_session.create_session()
    return db_sess.query(Student).get(user_id)


@app.route('/logout')
@login_required
def logout():
    """Выход пользователя"""
    logout_user()
    return redirect('/')


@app.route("/")
@app.route("/main")
def main_page():
    """Главная страница"""
    return render_template("base.html", title="Главная страница", items=[])


@app.route("/students")
def student_page():
    """Страница со студентами"""
    db_sess = db_session.create_session()
    students = db_sess.query(Student)
    return render_template("student_page.html", title="Студенты", items=students)


@app.route("/projects")
def project_page():
    """Страница с проектами компаний"""
    db_sess = db_session.create_session()
    projects = db_sess.query(CompanyProject)
    return render_template("projects_page.html", title="Проекты", items=projects)


@app.route("/burse")
def burse_page():
    """Страница с проектами студентов"""
    db_sess = db_session.create_session()
    projects = db_sess.query(StudentProject)
    return render_template("burse_page.html", title="Биржа",  items=projects)


@app.route('/student/<username>')
def student_profile(username):
    """Страница с профилем студента"""
    db_sess = db_session.create_session()
    user = db_sess.query(Student).filter(Student.username == username).first()  # поиск по логину
    if user:
        return render_template('user_profile.html', title='Профиль студента', user=user, news=user.projects)
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.route('/company/<username>')
def company_profile(username):
    """Страница с профилем компании"""
    db_sess = db_session.create_session()
    user = db_sess.query(Student).filter(Student.username == username).first()  # поиск по логину
    if user:
        return render_template('user_profile.html', title='Профиль компании', user=user, news=user.projects)
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    """Страница с формой регистрации"""
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data.strip():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают!")
        db_sess = db_session.create_session()
        if db_sess.query(Student).filter(Student.email == form.email.data.strip()).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть!")
        if db_sess.query(Student).filter(Student.username == form.username.data.strip()).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть!")
        if form.tip.data == 'СТУДЕНТ':
            user = Student(username=form.username.data.strip(), email=form.email.data.strip())
            user.set_password(form.password.data.strip())
            db_sess.add(user)
            db_sess.commit()
            return redirect(f'/student_register/{user.username}')
        else:
            user = Company(username=form.username.data.strip(), email=form.email.data.strip())
            user.set_password(form.password.data.strip())
            db_sess.add(user)
            db_sess.commit()
            return redirect(f'/company_register/{user.username}')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/student_register/<username>', methods=['GET', 'POST'])
def student_register(username):
    form = StudentRegisterForm()
    db_sess = db_session.create_session()
    student = db_sess.query(Student).filter(Student.username == username).first()
    if student:
        if form.validate_on_submit():
            student.name = form.name.data.strip()
            student.surname = form.surname.data.strip()
            student.birthday = form.birthday.data
            student.study_place = form.study_place.data.strip()
            student.program = form.program.data.strip()
            student.grade = form.grade.data
            student.course = form.course.data
            file = form.photo.data
            if file:
                filename = secure_filename(file.filename)
                os.chdir('static/' + app.config['STUDENT_PHOTO_FOLDER'])
                if not os.path.isdir(student.username):
                    os.mkdir(student.username)
                student.photo_path = url_for(
                    'static', filename=app.config['STUDENT_PHOTO_FOLDER'] + f'{student.username}/{filename}')
                file.save(f'{student.username}/{filename}')
            return redirect('/login')
    else:
        abort(404)
    return render_template('student_register.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Страница с формой авторизации пользователя"""
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(Student).filter((Student.email == form.email.data.strip())).first()
        if not user:
            user = db_sess.query(Company).filter((Company.email == form.email.data.strip())).first()
        if user and user.check_password(form.password.data.strip()):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


# @app.route('/add_news',  methods=['GET', 'POST'])
# @login_required
# def add_news():
#     """Страница с формой добавления записи"""
#     form = CompanyProjectForm()
#     if form.validate_on_submit():
#         db_sess = db_session.create_session()
#         news = News()
#         news.title = form.title.data.strip()
#         news.content = form.content.data.strip()
#         news.is_private = form.is_private.data
#         file = form.photo.data  # загрузка файла (изображения)
#         if file:
#             filename = secure_filename(file.filename)
#             news.photo_path = url_for('static', filename=app.config['NEWS_PHOTO_FOLDER'] + filename)
#             file.save(f'static/img/news_photos/{filename}')  # сохранение файла
#         current_user.projects.append(news)
#         db_sess.merge(current_user)
#         db_sess.commit()
#         return redirect(f'/user/{news.user.username}')
#     return render_template('projects.html', title='AstroCat',
#                            form=form)
#
#
# @app.route('/edit_news/<int:id>', methods=['GET', 'POST'])
# @login_required
# def edit_news(id):
#     """Страница с формой редактирования записи"""
#     form = CompanyProjectForm()
#     if request.method == "GET":
#         db_sess = db_session.create_session()
#         news = db_sess.query(News).filter(News.id == id,
#                                           News.user == current_user
#                                           ).first()
#         if news:
#             form.title.data = news.title
#             form.content.data = news.content
#             form.is_private.data = news.is_private
#         else:
#             abort(404)
#     if form.validate_on_submit():
#         db_sess = db_session.create_session()
#         news = db_sess.query(News).filter(News.id == id,
#                                           News.user == current_user
#                                           ).first()
#         if news:
#             news.title = form.title.data.strip()
#             news.content = form.content.data.strip()
#             news.is_private = form.is_private.data
#             file = form.photo.data
#             if file:
#                 if news.photo_path:
#                     os.remove(news.photo_path[1:])
#                 filename = secure_filename(file.filename)
#                 news.photo_path = url_for('static', filename=app.config['NEWS_PHOTO_FOLDER'] + filename)
#                 file.save(f'static/img/news_photos/{filename}')
#             db_sess.commit()
#             return redirect(f'/user/{news.user.username}')
#         else:
#             abort(404)
#     return render_template('projects.html',
#                            title='AstroCat',
#                            form=form, photo=news.photo_path
#                            )
#
#
# @app.route('/delete_news/<int:id>', methods=['GET', 'POST'])
# @login_required
# def delete_news(id):
#     """Удаление записи"""
#     db_sess = db_session.create_session()
#     news = db_sess.query(News).filter(News.id == id,
#                                       News.user == current_user
#                                       ).first()
#     if news:
#         user = news.user
#         if news.photo_path:  # если было изображение
#             os.remove(news.photo_path[1:])  # удаляем
#         db_sess.delete(news)  # удаление
#         db_sess.commit()
#         return redirect(f'/user/{user.username}')
#     else:
#         abort(404)
#
# @app.route('/edit_user/<username>', methods=['GET', 'POST'])
# @login_required
# def edit_user(username):
#     """Страница с формой редактирования пользователя"""
#     form = EditCompanyForm()
#     if request.method == "GET":
#         db_sess = db_session.create_session()
#         user = db_sess.query(User).filter(User.username == username).first()
#         if user:
#             form.username.data = user.username
#             form.name.data = user.name
#             form.surname.data = user.surname
#             form.age.data = user.age
#             form.about.data = user.about
#         else:
#             abort(404)
#     if form.validate_on_submit():
#         db_sess = db_session.create_session()
#         user = db_sess.query(User).filter(User.username == username).first()
#         if user:
#             new_user = db_sess.query(User).filter(User.username == form.username.data.strip()).first()
#             if new_user and new_user != user:
#                 return render_template('user.html', title='AstroCat',
#                                        form=form,
#                                        message="Логин занят!")
#             user.username = form.username.data.strip()
#             user.name = form.name.data.strip()
#             user.surname = form.surname.data.strip()
#             user.age = form.age.data
#             user.about = form.about.data.strip()
#             db_sess.commit()
#             return redirect(f'/user/{user.username}')
#         else:
#             abort(404)
#     return render_template('user.html',
#                            title='AstroCat',
#                            form=form
#                            )


if __name__ == '__main__':
    main()
