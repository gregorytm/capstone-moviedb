from flask import Flask, request, render_template, jsonify, session, redirect, flash
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

@app.route("/")
def homepage():
    """homepage"""
    return render_template('home.html')


# movies search & details endpoint 
@app.route("/api/movies", methods=["GET"])
def endpoint():
    """api backend"""
    movies = []
    search = request.args['title']
    res = requests.get("https://api.themoviedb.org/3/search/movie", params={'api_key': API_KEY, 'query': search})
    data = res.json()
    
    for result in data['results']: 
        movie_info = {}
        movie_info["title"] = result['title']

        movie_info["overview"] = result['overview']

        movie_info["poster_path"] = result['poster_path']

        movie_info["release_date"] = result['release_date']

        movie_info["vote_average"] = result['vote_average']

        movie_info['id'] = result['id']

        movies.append(movie_info)
    return jsonify(movies)

#movie details
@app.route("/api/movies/<id>", methods=["GET"])
def title_page(id):
    movie = get_movie_by_id(id)
    return render_template("details.html", movie=movie)

# add to watchlist
@app.route('/api/movies/<id>', methods=["POST"])
def add_watchlist(id):

    session_id = session['id']
    print("-!")
    print(session_id)
    print("--!")

    user=User.query.get(session_id)
    print(user.username)
    print("---!")

    print(id)
    check = Movie.query.filter_by(tmdb_id=id)
    print('----!')
    print(check)

    if check == True:
        print('----!')
        print(id)
        local_movie = Movie.query.get(id)
        print(local_movie)
        user.to_watch.append(local_movie)
        db.session.add(user)
        db.session.commit()
        return redirect(f"/users/{session_id}/watchlist")
    else:

        movie = get_movie_by_id(id)
        print(movie)
        
        user.to_watch.append(movie)
        db.session.add(user)
        db.session.commit()

        return redirect(f"/users/{session_id}/watchlist")


# user watchlist
@app.route(f'/users/<int:id>/watchlist', methods=["GET", "POST"])
def watchlist(id):

    user = User.query.get_or_404(id)
    if 'id' not in session:
        flash("Access unauthorized", "danger")
        return redirect('/users/login')
    else:
        return render_template('watchlist.html', user=user)


# user register, login/out, user details page & delete user
@app.route("/users/register", methods=["GET", "POST"])
def new_user():
    
    if 'id' in session:
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

        return redirect('/')
    else:
        return render_template("users/register.html", form=form)


@app.route('/users/login', methods=['GET', 'POST'])
def login():

    if 'id' in session:
        return redirect('/')

    form = LoginForm()

    if form.validate_on_submit():
        print(form.errors)
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username, password)
        if user:
            session['id'] = user.id
            return redirect('/')
        else:
            flash('incorrect login')
            return render_template("users/login.html", form=form)
    else:
        return render_template("users/login.html", form=form)

@app.route("/users/logout")
def logout():
    if "id" in session:
        session.pop('id')
        flash("logged out sucessfully")
        print("logged out successfully")
        return redirect("/")
    else:
        return redirect("/")

@app.route('/users/<int:id>', methods=["GET", "POST"])
def update_profile(id):

    user = User.query.get_or_404(id)

    if 'id' not in session:
        flash("Access unauthorized", "danger")
        return redirect('/users/login')
    
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


@app.route('/users/delete/<int:id>', methods=["POST"])
def delete_todo(id):
    user = User.query.get_or_404(id)

    if 'id' not in session:
        flash("Access unauthorized", "danger")
        return redirect('/users/login')

    form=DeleteForm()

    db.session.delete(user)
    db.session.commit()
    session.pop("id")
    flash ('user deleted')

    return redirect('/')

#make movie api call
def get_movie_by_id(id):
    res = requests.get("https://api.themoviedb.org/3/movie/" + id, params = {'api_key': API_KEY})

    data = res.json()

    return Movie(tmdb_id=data["id"], title=data["title"], overview=data["overview"], poster_path=data["poster_path"], release_date=data["release_date"], vote_average=data["vote_average"])


