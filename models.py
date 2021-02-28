from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()
db = SQLAlchemy()

class User(db.Model):
    __tablename__="users"

    id= db.Column(db.Integer, 
                        primary_key=True)
    username=db.Column(db.Text, 
                        nullable=False, 
                        unique=True)
    password = db.Column(db.Text,
                        nullable=False)
    img = db.Column(db.Text, 
                        nullable=False,
                        default="static/images/default_user.jpeg")
    to_watch = db.relationship('Movie', secondary='my_watchlist')
    

    @classmethod
    def register(cls, username, password, img):
        """hash user password"""

        hashed = bcrypt.generate_password_hash(password)
        hashed_utf8 = hashed.decode("utf8")
        user = cls(
            username=username,
            password=hashed_utf8,
            img=img
        )

        db.session.add(user)
        return user

    @classmethod
    def authenticate(cls, username, password):

        user = User.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password, password):
            return user
        else:
            return False

class Review(db.Model):
    __tablename__="reviews"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    movie_id = db.Column(db.Integer, db.ForeignKey('movies.id'))
    comments = db.Column(db.String(150))
    rating = db.Column(db.Integer)

class Movie(db.Model):
    __tablename__="movies"
    id=db.Column(db.Integer, primary_key=True)
    movie_id=db.Column(db.Integer)
    overview=db.Column(db.Text)
    title=db.Column(db.Text)
    release_date=db.Column(db.DateTime)
    poster_path = db.Column(db.Text)
    vote_average = db.Column(db.Integer)

class Watchlist(db.Model):
    __tablename__="my_watchlist"
    id=db.Column(db.Integer, primary_key=True)
    user_id=db.relationship(db.Integer, db.ForeignKey('users.id'))
    movie_id=db.relationship(db.Integer, db.ForeignKey('movies.id'))

def connect_db(app):
    """connect the db"""
    
    db.app = app
    db.init_app(app)