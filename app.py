from flask import Flask, request, render_template, jsonify, session, redirect
from models import db, connect_db, User, Review, Movie, Watchlist
from flask_sqlalchemy import SQLAlchemy
from forms import UserForm, LoginForm
import requests
import os

app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///movies_capstone'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False

db = SQLAlchemy()
db.app = app
db.init_app(app)

# never useed this before but it works
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY

API_KEY = "bda83f15a6dbfe7dedc91a90383a8b38"

@app.route("/")
def homepage():
    """homepage"""
    return render_template('home.html')

@app.route("/api/movies", methods=["GET"])
def endpoint():
    """api backend"""
    movies = []
    search = request.args['title']
    res = requests.get("https://api.themoviedb.org/3/search/movie", params={'api_key': API_KEY, 'query': search})
    data = res.json()
    
    for result in data['results']: 
        movie_info = {}
        movie_info["title"] = result['original_title']

        movie_info["overview"] = result['overview']

        movie_info["poster_path"] = result['poster_path']

        movie_info["release_date"] = result['release_date']

        movie_info["vote_average"] = result['vote_average']

        movie_info['id'] = result['id']

        movie_info['genre_ids'] = result['genre_ids']

        movies.append(movie_info)
    return jsonify(movies)

@app.route("/register", methods=["GET", "POST"])
def new_user():
    
    if 'id' in session:
        return redirect("/")

    form = UserForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.user.data
        img = form.img.data

        user = User.register(username, password, img)

        db.session.commit()
        session['id'] = user.id

        return render_template('home.html')
    else:
        return render_template("users/register.html", form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():

    if 'id' in session:
        return redirect('/')

    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username, password)
        if user:
            session['id'] = user.id
            return redirect(f'/users/{user.id}')
        else:
            form.username.erros = [ "Invalid username/password."]
            return render_template("users/login.html", form=form)

    return render_template("users/login.html", form=form)

@app.route("/logout")
def logout():
    if "id" in session:
        session.pop('id')
        return redirect("/login")
    else:
        return redirect("/login")


@app.route("/api/movies/search/<id>")
def title_page(id):
    id = id

    res = requests.get("https://api.themoviedb.org/3/movie/11?api_key=bda83f15a6dbfe7dedc91a90383a8b38&language=en-US")
    data = res.json()

    return data
    # return render_template("details.html", id = title)
