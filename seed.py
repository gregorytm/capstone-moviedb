from app import app
from models import db, User, Movie, Watchlist, Review, User

db.drop_all()
db.create_all()

# Empty table
# User.query.delete()

movie1 = Movie(
    id=1,
    overview="long time ago!",
    title="Star Wars",
    release_year="1987"
)

db.session.add(movie1)
db.session.commit()

u1 = User.register(
    username="jokerbob",
    password="jokerbob",
    img="static/images/default_user.jpeg"
)

u2 = User.register(
    username="jillygal",
    password="jillygal",
    img="static/images/default_user.jpeg"
)

db.session.add_all([u1,u2])
db.session.commit()

review1 = Review(
    user_id=1,
    movie_id=1,
    comments="its ok",
    rating=7.2
)

watchlist1 = Watchlist(
    user_id=1,
    movie_id=1,
)

db.session.add_all([watchlist1, review1])
db.session.commit()