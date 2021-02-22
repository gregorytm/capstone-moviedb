from app import app
from models import db, User, Movie, Watchlist, Review

db.drop_all()
db.create_all()

# Empty table
User.query.delete()

u1 = User(
    id=1,
    username="jokerbob",
    password="jokerbob",
    email = 'bobsmith@wayneEnterpriese.com',
    to_watch = 1
)

u2 = User(
    id=2,
    username="jillygal",
    password="jillygal",
    email="jillysmith@wayneEnerprises.com"
)

movie1 = Movie(
    id=1,
    overview="long time ago",
    title="Star Wars",
    genre=71,
    release_year="1987"
)

watchlist1 = Watchlist(
    id=1,
    user_id=1,
    movie_id=1
)

review1 = Review(
    id=1,
    user_id=1,
    movie_id=1,
    comments="its ok",
    rating=7.2
)

db.session.add_all([movie1, watchlist1, review1])
db.session.commit()

db.session.add_all([ul, u2])
db.session.commit()