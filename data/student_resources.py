from flask import jsonify, request
from flask_restful import abort, Resource
from data import db_session
from data.students import Student
from data.parsers import user_parser


class StudentsResource(Resource):
    """Ресурс пользователя (restful-api)"""

    def get(self, user_id):
        """Получение пользователя"""
        abort_if_user_not_found(user_id)
        session = db_session.create_session()
        user = session.query(Student).get(user_id)
        return jsonify(
            {
                'user':
                    user.to_dict(
                        only=(
                            'username', 'surname', 'name', 'age', 'about', 'email'))
            }
        )

    def post(self, user_id):
        """Изменение пользователя"""
        abort_if_user_not_found(user_id)
        args = user_parser.parse_args()
        session = db_session.create_session()
        user = session.query(Student).get(user_id)
        user.username = args['username']
        user.surname = args['surname']
        user.name = args['name']
        user.age = args['age']
        user.about = args['about']
        user.email = args['email']
        user.set_password(args['password'])
        session.commit()
        return jsonify({'success': 'OK'})

    def delete(self, user_id):
        """Удаление пользователя"""
        abort_if_user_not_found(user_id)
        session = db_session.create_session()
        user = session.query(Student).get(user_id)
        session.delete(user)
        session.commit()
        return jsonify({'success': 'OK'})


class UsersListResource(Resource):
    """Ресурс списка пользователей (restful-api)"""

    def get(self):
        """Получение всех пользователей"""
        session = db_session.create_session()
        users = session.query(Student).all()
        return jsonify(
            {
                'users':
                    [item.to_dict(
                        only=(
                            'username', 'surname', 'name', 'age', 'about', 'email'))
                        for item in users]
            }
        )

    def post(self):
        """Создание пользователя"""
        args = user_parser.parse_args()
        session = db_session.create_session()
        user = Student(
            username=args['username'],
            surname=args['surname'],
            name=args['name'],
            age=args['age'],
            about=args['about'],
            email=args['email']
        )
        user.set_password(request.json['password'])
        session.add(user)
        session.commit()
        return jsonify({'success': 'OK'})


def abort_if_user_not_found(user_id):
    """Обработка ситуации, когда пользователя с указанным id не существует"""
    session = db_session.create_session()
    user = session.query(Student).get(user_id)
    if not user:
        abort(404, message=f"Student {user_id} not found")
