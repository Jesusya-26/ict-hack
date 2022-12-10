from flask_restful import Resource, abort
from flask import jsonify
from data import db_session
from data.student_projects import StudentProject
from data.parsers import student_projects_parser


class StudentProjectResource(Resource):
    """Ресурс записи (restful-api)"""

    def get(self, news_id):
        """Получение записи"""
        abort_if_news_not_found(news_id)
        session = db_session.create_session()
        news = session.query(StudentProject).get(news_id)
        return jsonify({'news': news.to_dict(
            only=('title', 'content', 'user.name', 'is_private', 'photo_path'))})  # возвращаем json

    def post(self, news_id):
        """Изменение записи"""
        abort_if_news_not_found(news_id)
        args = student_projects_parser.parse_args()  # парсер аргументов
        session = db_session.create_session()
        news = session.query(StudentProject).get(news_id)
        news.title = args['title']
        news.content = args['content']
        news.is_private = args['is_private']
        news.user_id = args['user_id']
        session.commit()
        return jsonify({'success': 'OK'})  # возвращаем json {ok}

    def delete(self, news_id):
        """Удаление записи"""
        abort_if_news_not_found(news_id)
        session = db_session.create_session()
        news = session.query(StudentProject).get(news_id)
        session.delete(news)
        session.commit()
        return jsonify({'success': 'OK'})


class NewsListResource(Resource):
    """Ресурс списка записей (restful-api)"""

    def get(self):
        """Получение всех записей"""
        session = db_session.create_session()
        news = session.query(StudentProject).all()
        return jsonify({'news': [item.to_dict(
            only=('title', 'content', 'user.name', 'photo_path')) for item in
            news]})  # возвращаем json со всеми записями

    def post(self):
        """Публикация новой записи"""
        args = student_projects_parser.parse_args()
        session = db_session.create_session()
        news = StudentProject(
            title=args['title'],
            content=args['content'],
            user_id=args['user_id'],
            is_private=args['is_private']
        )
        session.add(news)
        session.commit()
        return jsonify({'success': 'OK'})


def abort_if_news_not_found(news_id):
    """Обработка в ситуации, когда записи с указанным id не существует"""
    session = db_session.create_session()
    news = session.query(StudentProject).get(news_id)
    if not news:
        abort(404, message=f"StudentProject {news_id} not found")  # ошибка 404, json {not found}
