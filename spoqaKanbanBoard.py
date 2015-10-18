#-*-coding: utf-8-*-
__author__ = 'dongsamb'
import flask
import flask.ext.sqlalchemy
import flask.ext.restless
from sqlalchemy.orm import relationship, backref

# Create the Flask application and the Flask-SQLAlchemy object.
app = flask.Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Board.db'
db = flask.ext.sqlalchemy.SQLAlchemy(app)


# 추후 개발
# class User(db.Model):
#     __tablename__ = 'user'
#
#     # Scehma
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.Unicode, unique=True)
#     joined_date = db.Column(db.Date)


# 보드 table
class Board(db.Model):
    __tablename__ = 'board'

    # Scehma
    id = db.Column(db.Integer, primary_key=True)
    # owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    # owner = db.relationship('User', backref=db.backref('borders', lazy='dynamic'))
    # created_date = db.Column(db.Date)

    # Relations
    lists = relationship("List", secondary="board_lists", backref=backref("board"))

# 보드->리스트 one2many relation
class Board_Lists(db.Model):
    __tablename__ = 'board_lists'

    # Scehma
    board_id = db.Column(db.Integer, db.ForeignKey('board.id'), primary_key=True)
    list_id = db.Column(db.Integer, db.ForeignKey('list.id'), primary_key=True)

# 리스트 table
class List(db.Model):
    __tablename__ = 'list'

    # Scehma
    id = db.Column(db.Integer, primary_key=True)
    board_id = db.Column(db.Integer, db.ForeignKey('board.id'))

    # Relations
    cards = relationship("Card", secondary="list_cards", backref=backref("card"))

# 리스트->카드 one2many relation
class List_Cards(db.Model):
    __tablename__ = 'list_cards'

    # Scehma
    list_id = db.Column(db.Integer, db.ForeignKey('list.id'), primary_key=True)
    card_id = db.Column(db.Integer, db.ForeignKey('card.id'), primary_key=True)

class Card(db.Model):
    __tablename__ = 'card'

    # Scehma
    id = db.Column(db.Integer, primary_key=True)
    list_id = db.Column(db.Integer, db.ForeignKey('list.id'))
    title = db.Column(db.Unicode)


# Create the database tables.
db.create_all()

# Create the Flask-Restless API manager.
manager = flask.ext.restless.APIManager(app, flask_sqlalchemy_db=db)

# Create API endpoints, which will be available at /api/<tablename> by
# default. Allowed HTTP methods can be specified as well.
manager.create_api(Board, methods=['GET', 'POST', 'DELETE'])
manager.create_api(List, methods=['GET', 'POST', 'DELETE'])
manager.create_api(Card, methods=['GET', 'POST', 'DELETE'])


@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
