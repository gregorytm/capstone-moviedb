from app import app
from models import db, User, Movie, Watchlist, Review, User

db.drop_all()
db.create_all()

# Empty table
# User.query.delete()

movie1 = Movie(
    movie_id = 1,
    overview="long time ago!",
    title="Star Wars",
    # release_date="1987"
)

db.session.add(movie1)

u1 = User.register(
    username="jokerbob",
    password="jokerbob",
    img="static/images/default_user.jpeg",
    # to_watch=1
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

db.session.add(review1)
db.session.commit()

watchlist1 = Watchlist(
    user_id=1,
    movie_id=1,
)

db.session.add(watchlist1)
db.session.commit()