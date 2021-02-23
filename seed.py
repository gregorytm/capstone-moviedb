from app import app
from models import db, User, Movie, Watchlist, Review

db.drop_all()
db.create_all()

# Empty table
User.query.delete()

movie1 = Movie(
    id=1,
    overview="long time ago!",
    title="Star Wars",
    release_year="1987"
    # genre=[
    #     12,
    #     28,
    #     878
    # ]
)

db.session.add(movie1)
db.session.commit()

u1 = User(
    id=1,
    username="jokerbob",
    password="jokerbob",
    # to_watch = 1
)

u2 = User(
    id=2,
    username="jillygal",
    password="jillygal",
    # to_watch=1
)

db.session.add_all([u1,u2])
db.session.commit()

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

db.session.add_all([watchlist1, review1])
db.session.commit()