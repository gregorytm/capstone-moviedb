from flask import Flask, request, render_template, jsonify, session, redirect, flash, Markup
from models import db, connect_db, User, Movie, Watchlist
from flask_sqlalchemy import SQLAlchemy
from forms import UserForm, LoginForm, EditUserForm, DeleteForm

import requests

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///movies_capstone'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['SECRET_KEY'] = "oh-yes-51015"

connect_db(app)

API_KEY = "bda83f15a6dbfe7dedc91a90383a8b38"

# home route
@app.route("/")
def homepage():
    """homepage"""
    return render_template('base.html')

# movies search 
@app.route("/api/movies", methods=["GET"])
def endpoint():
    """api backend"""
    movies = []
    search = request.args['title']
    
    if len(search) == 0:
        return redirect ('/')
    
    res = requests.get("https://api.themoviedb.org/3/search/movie", params={'api_key': API_KEY, 'query': search})
    data = res.json()
    
    for result in data['results']: 
        movie_info = {}
        movie_info["title"] = result['title']

        movie_info["overview"] = result['overview']

        movie_info["poster_path"] = result['poster_path']

        movie_info["release_date"] = result['release_date'][:4]
        print(type(movie_info["release_date"]))
        print(movie_info["release_date"])

        movie_info["vote_average"] = result['vote_average']

        movie_info['id'] = result['id']

        movies.append(movie_info)
    return render_template("search.html", movies=movies)

# movie details
@app.route("/api/movies/<id>", methods=["GET"])
def title_page(id):
    movie = get_movie_by_id(id)
    movie.release_date = movie.release_date[:4]
    return render_template("details.html", movie=movie)

# add to watchlist
@app.route('/api/movies/<id>', methods=["POST"])
def add_watchlist(id):

    session_id = session['id']

    user=User.query.get(session_id)

    if 'id' not in session:
        flash(Markup('Log in to enjoy the Watchlist feature.  Not a user, Create one <a href="/users/register" class="alert-link">here</a>'), 'success')
        return redirect("/users/login")

    existing_movie = Movie.query.filter_by(tmdb_id=id).first()

    if existing_movie != None:
        # use existing_movie to check if the movie already is in the DB, add existing movie to user's watchlist
        user.to_watch.append(existing_movie)
        db.session.add(user)
        db.session.commit()
        return redirect("/watchlist")
    else:
        # if movie is not in DB, add movie to our movieDB then add it to user watchlist
        movie = get_movie_by_id(id)
        movie.release_date = movie.release_date[:4]
        print(movie)
        
        user.to_watch.append(movie)
        db.session.add(user)
        db.session.commit()

        return redirect("/watchlist")

# user watchlist
@app.route(f'/watchlist', methods=["GET", "POST"])
def watchlist():

    if 'id' not in session:
        flash("Access unauthorized", "danger")
        return redirect('/users/login')
    else:
        user = User.query.get_or_404(session["id"])
        return render_template('watchlist.html', user=user)


# delete movie from watchlist
@app.route(f'/watchlist/<int:tmdb_id>/delete', methods=["POST"])
def delete_moive( tmdb_id):

    if 'id' not in session:
        flash("Access unauthorized", "danger")
        return redirect('/users/login')

    user=User.query.get_or_404(session['id'])
    movie=Movie.query.get_or_404(tmdb_id)

    if movie in user.to_watch:
        user.to_watch.remove(movie)
        db.session.commit()
        return redirect("/watchlist")

    else:  
        flash('no movie', 'error')
        return redirect("/watchlist")
    
# user register
@app.route("/users/register", methods=["GET", "POST"])
def new_user():
    
    if 'id' in session:
        flash(f'Already logged in', 'success')
        return redirect("/")

    form = UserForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        img = form.img.data
        if len(img) == 0:
            img=None

        user = User.register(username, password, img)

        db.session.add(user)
        db.session.commit()
        session['id'] = user.id

        flash('Register Success', 'success')
        return redirect('/')
    else:
        return render_template("users/register.html", form=form)

# loggin in to  profile
@app.route('/users/login', methods=['GET', 'POST'])
def login():

    if 'id' in session:
        flash('Already logged in', 'error')
        return redirect('/')
    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username, password)
        if user:
            session['id'] = user.id
            flash('Login Successful', 'success')
            return redirect('/')
        else:
            flash('incorrect login', 'error')
            return render_template("users/login.html", form=form)
    else:
        return render_template("users/login.html", form=form)

# user logout
@app.route("/users/logout")
def logout():
    if "id" in session:
        session.pop('id')
        flash("logged out sucessfully", 'success')
        return redirect("/")
    else:
        return redirect("/")

# user edit page
@app.route('/users/edit', methods=["GET", "POST"])
def update_profile():

    if 'id' not in session:
        flash("Access unauthorized", "danger")
        return redirect('/users/login')

    user = User.query.get_or_404(session['id'])
    
    username = user.username
    img = user.img

    form = EditUserForm(obj=user)
    
    if form.validate_on_submit():

        if len(form.username.data) == 0:
            user.username= user.username
        else:
            user.username=form.username.data

        if len(form.img.data) == 0:
            user.img = user.img
        else:
            user.img=form.img.data

        db.session.commit()
        flash('update sucessful')

        return redirect("/")
    else:
        return render_template("users/edit.html", form=form, user=user)

# delete account
@app.route('/users/delete', methods=["POST"])
def delete_todo():

    if 'id' not in session:
        flash("Access unauthorized", "danger")
        return redirect('/users/login')
        
    user = User.query.get_or_404(session['id'])

    form=DeleteForm()

    db.session.delete(user)
    db.session.commit()
    session.pop("id")
    flash ('user deleted')

    return redirect('/')

# make api call using the movie id
def get_movie_by_id(id):
    res = requests.get("https://api.themoviedb.org/3/movie/" + id, params = {'api_key': API_KEY})

    data = res.json()

    return Movie(tmdb_id=data["id"], title=data["title"], overview=data["overview"], poster_path=data["poster_path"], release_date=data["release_date"], vote_average=data["vote_average"])


