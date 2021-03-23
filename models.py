import os
import json
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import Column, String, create_engine, Integer


# database_path = os.environ['DATABASE_URL']
database_path = os.environ.get('DATABASE_URL')
if not database_path:
    database_name = "agency"
    database_path = "postgres://{}/{}".format('localhost:5432', database_name)

db = SQLAlchemy()
migrate = Migrate()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''


def setup_db(app, database_path=database_path, test=False):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    if(test):
        db.create_all()
    else:
        migrate.init_app(app, db)


def insert_db(model: db.Model) -> bool:
    success = True
    try:
        db.session.add(model)
        db.session.commit()
    except Db.false:
        success = False
        db.session.rollback()
    finally:
        db.session.close()
        return success


def update_db() -> bool:
    success = True
    try:
        db.session.commit()
    except Db.false:
        db.session.rollback()
        success = False
    finally:
        db.session.close()
        return success


def delete_db(model: db.Model) -> bool:
    success = True
    try:
        db.session.delete(model)
        db.session.commit()
    except Db.false:
        success = False
        db.session.rollback()
    finally:
        db.session.close()
        return success


class Movie(db.Model):
    __tablename__ = 'Movie'

    id = db.Column(Integer, primary_key=True)
    title = db.Column(String)
    release_date = db.Column(String)

    def __init__(self, title, release_date=""):
        self.title = title
        self.release_date = release_date

    def insert(self) -> bool:
        return insert_db(self)

    def update(self) -> bool:
        return update_db()

    def delete(self) -> bool:
        return delete_db(self)

    def format(self):
        return {'id': self.id,
                'title': self.title,
                'release_date': self.release_date}

    def __repr__(self):
        return f'<Movie ID: {self.id}, title: {self.title}>'


class Actor(db.Model):
    __tablename__ = 'Actor'
    id = db.Column(Integer, primary_key=True)
    name = db.Column(String)
    age = db.Column(Integer)
    gender = db.Column(String)

    def __init__(self, name, age, gender):
        self.name = name
        self.age = age
        self.gender = gender

    def insert(self) -> bool:
        return insert_db(self)

    def update(self) -> bool:
        return update_db()

    def delete(self) -> bool:
        return delete_db(self)

    def format(self):
        return {'id': self.id,
                'name': self.name,
                'age': self.age,
                'gender': self.gender}

    def __repr__(self):
        return f'<Actor ID: {self.id}, name: {self.name}>'
