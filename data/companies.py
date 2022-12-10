import datetime
import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin
from data.db_session import SqlAlchemyBase
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class Company(SqlAlchemyBase, UserMixin, SerializerMixin):
    """Модель пользователя"""
    __tablename__ = 'companies'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    username = sqlalchemy.Column(sqlalchemy.String, unique=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    surname = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    age = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    about = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    email = sqlalchemy.Column(sqlalchemy.String,
                              index=True, unique=True)
    hashed_password = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                     default=datetime.datetime.now)
    news = orm.relation("CompanyProject", back_populates='company')

    def set_password(self, password):
        """Хэширование пароля"""
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        """Сравнение хэшей введённого пароля с установленным"""
        return check_password_hash(self.hashed_password, password)

    def __repr__(self):
        return f'<Company> {self.username}'
