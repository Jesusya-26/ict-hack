import os
from flask import Flask, render_template, redirect
from flask_login import LoginManager, login_required, logout_user
from flask_restful import Api
from data import db_session
from data.students import Student
from data.student_projects import StudentProject

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
api = Api(app)


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
    return redirect("/")  # перевод на главную страницу


@app.route("/")
@app.route("/main")
def main_page():
    """Главная страница"""
    db_sess = db_session.create_session()
    projects = db_sess.query(StudentProject)
    return render_template("main_page.html", title="Главная страница", projects=projects)


@app.route("/students")
def student_page():
    """Главная страница"""
    db_sess = db_session.create_session()
    projects = db_sess.query(StudentProject)
    return render_template("main_page.html", title="Студенты", projects=projects)


@app.route("/projects")
def project_page():
    """Главная страница"""
    db_sess = db_session.create_session()
    projects = db_sess.query(StudentProject)
    return render_template("main_page.html", title="Проекты", projects=projects)


@app.route("/burse")
def burse_page():
    """Главная страница"""
    db_sess = db_session.create_session()
    projects = db_sess.query(StudentProject)
    return render_template("main_page.html", title="Биржа", projects=projects)


if __name__ == '__main__':
    main()
