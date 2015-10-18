#-*-coding: utf-8-*-
__author__ = 'dongsamb'
import flask
import flask.ext.sqlalchemy
import flask.ext.restless
from sqlalchemy.orm import relationship, backref
import datetime

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

# 카드 table
class Card(db.Model):
    __tablename__ = 'card'

    # Scehma
    id = db.Column(db.Integer, primary_key=True)
    list_id = db.Column(db.Integer, db.ForeignKey('list.id'))
    title = db.Column(db.Unicode)

    # fucntion
    def __init__(self, list_id, title):
        self.list_id = list_id
        self.title = title

    def __repr__(self):
        return '<{} card, parent list:{}>'.format(self.title,self.list_id)


# 리스트 table
class List(db.Model):
    __tablename__ = 'list'

    # Scehma
    id = db.Column(db.Integer, primary_key=True)
    board_id = db.Column(db.Integer, db.ForeignKey('board.id'))

    # Relations
    cards = relationship(Card, secondary="list_cards", backref=backref("card"), lazy='dynamic')

    # fucntion
    def __init__(self, board_id, card=""):
        self.board_id = board_id
        # self.cards = card

    def __repr__(self):
        return '<list, parent board:{}>'.format(self.board_id)


# 보드 table
class Board(db.Model):
    __tablename__ = 'board'

    # Scehma
    id = db.Column(db.Integer, primary_key=True)
    created_date = db.Column(db.Date)
    # owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    # owner = db.relationship('User', backref=db.backref('borders', lazy='dynamic'))

    # Relations
    lists = relationship(List, secondary="board_lists", backref=backref("board"), lazy='dynamic')

    # fucntion
    def __init__(self, created_date=datetime.date.today().strftime('%d-%m-%y')):
        self.created_date = created_date

    def __repr__(self):
        return '<board, created {}>'.format(self.created_date)

# 보드->리스트 relation
class Board_Lists(db.Model):
    __tablename__ = 'board_lists'

    # Scehma
    board_id = db.Column(db.Integer, db.ForeignKey('board.id'), primary_key=True)
    list_id = db.Column(db.Integer, db.ForeignKey('list.id'), primary_key=True)

# 리스트->카드 relation
class List_Cards(db.Model):
    __tablename__ = 'list_cards'

    # Scehma
    list_id = db.Column(db.Integer, db.ForeignKey('list.id'), primary_key=True)
    card_id = db.Column(db.Integer, db.ForeignKey('card.id'), primary_key=True)

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
