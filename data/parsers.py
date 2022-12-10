from flask_restful import reqparse

user_parser = reqparse.RequestParser()  # парсер аргументов для ресурсов пользователя
user_parser.add_argument('username', required=True)
user_parser.add_argument('surname', required=True)
user_parser.add_argument('name', required=True)
user_parser.add_argument('age', type=int)
user_parser.add_argument('about')
user_parser.add_argument('email', required=True)
user_parser.add_argument('password', required=True)


student_projects_parser = reqparse.RequestParser()  # парсер аргументов для ресурсов записи
student_projects_parser.add_argument('title', required=True)
student_projects_parser.add_argument('content', required=True)
student_projects_parser.add_argument('is_private', required=True, type=bool)
student_projects_parser.add_argument('user_id', required=True, type=int)

company_parser = reqparse.RequestParser()  # парсер аргументов для ресурсов пользователя
company_parser.add_argument('username', required=True)
company_parser.add_argument('surname', required=True)
company_parser.add_argument('name', required=True)
company_parser.add_argument('age', type=int)
company_parser.add_argument('about')
company_parser.add_argument('email', required=True)
company_parser.add_argument('password', required=True)


company_projects_parser = reqparse.RequestParser()  # парсер аргументов для ресурсов записи
company_projects_parser.add_argument('title', required=True)
company_projects_parser.add_argument('content', required=True)
student_projects_parser.add_argument('is_private', required=True, type=bool)
company_projects_parser.add_argument('user_id', required=True, type=int)
