# b4g/database/models.py

from flask_login import UserMixin
from b4g import db


class Base(db.Model):
    """ Basic Table Structure """
    __abstract__ = True
    # __table_args__ = {'mysql_engine': 'InnoDB', 'mysql_charset': 'utf8'}
    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )
    date_created = db.Column(
        db.DateTime,
        default=db.func.current_timestamp()
    )
    date_modified = db.Column(
        db.DateTime,
        default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp()
    )


class Users(UserMixin, Base):
    """ User table """
    __tablename__ = 'users'

    email = db.Column(db.String(128), unique=True)
    username = db.Column(db.String(128))
    password = db.Column(db.String(128))
