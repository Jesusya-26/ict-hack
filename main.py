import os
from flask import Flask, render_template
from flask_login import LoginManager
from flask_restful import Api
from data import db_session

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
api = Api(app)


def main():
    """Запуск приложения"""
    db_session.global_init("db/astro-project.db")
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)


@app.route("/")
@app.route("/main")
def main_page():
    """Главная страница"""
    db_sess = db_session.create_session()
    return render_template("main_page.html", title="Главная страница")


if __name__ == '__main__':
    main()
