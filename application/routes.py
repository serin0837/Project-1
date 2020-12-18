from application import app, db
from application.models import Games, Add, Reviews, Review, Delete, Update
from flask import Flask, render_template, request, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField

@app.route('/add', methods=["GET", "POST"])
def add():
    form=Add()
    if request.method == 'POST':

        if not form.validate_on_submit():
            return render_template('adderror.html', form=form, title="New Game")
        else:
            new_game = Games(Title=form.Title.data, Release_date=form.Release_date.data, Genre=form.Genre.data, Age_rating=form.Age_rating.data, Description= form.Description.data)
            db.session.add(new_game)
            db.session.commit()
            return redirect(url_for("home"))
    return render_template('add.html', form=form, title="New Game")

@app.route('/home', methods=['GET', 'POST'])
@app.route('/', methods=['GET', 'POST'])
def home():
    all_games = Games.query.all()
    
    return render_template("index.html", title="Home", all_games=all_games)


@app.route('/game/<Title>', methods= ["GET", "POST"])
def game(Title):
    form=Add()
    game = Games.query.filter_by(Title=Title).first()
    a=0
    b=0
    for review in game.reviews:
        a+=review.Rating
        b+=1
    if b==0:
        d="No reviews have been posted"
    else:
        c= int(a/b*10)
        d=float(c/10)
    return render_template("update.html", form=form, title=Title, game=game, all_ratings=d)

@app.route('/review/<Title>', methods=["GET", "POST"])
def review(Title):
    form=Review()
    if request.method == 'POST':

        if not form.validate_on_submit():
            return render_template('reviewerror.html', form=form, title="New Game")
        else:
            new_review = Reviews(Games_title=Title, Review_title=form.Review_title.data, Reviewer_name=form.Reviewer_name.data, Review_password=form.Review_password.data, Review=form.Review.data, Rating= form.Rating.data)
            db.session.add(new_review)
            db.session.commit()
            return redirect(url_for("game", Title=new_review.Games_title))
    return render_template('review.html', form=form, title="New Game")

@app.route('/delete/<int:number>/<pword>')
def delete(number, pword):
    rev = Reviews.query.filter_by(Review_ID=number).first()
    r=rev.Games_title
    if rev is not None:
        db.session.delete(rev)
        db.session.commit()
        return redirect(url_for("game", Title=r))
    else:
        return "Entry does not exist"

@app.route('/edit/<int:number>', methods=["GET", "POST"])
def edit(number):
    form1=Delete()
    rev = Reviews.query.filter_by(Review_ID=number).first()
    r=rev.Games_title
    d= rev.Review_ID
    e=rev.Review_password
    if request.method == "POST":
        if form1.Review_password.data==rev.Review_password:
                return redirect(url_for("delete", number=d, pword=e))


    return render_template('delete.html', form1=form1, title=r)

@app.route('/update/<int:number>', methods=["GET", "POST"])
def update(number):
    form1=Update()
    rev = Reviews.query.filter_by(Review_ID=number).first()
    r=rev.Games_title
    d= rev.Review_ID
    e=rev.Review_password
    if request.method == "POST":
        if form1.Review_password.data==rev.Review_password:
            return redirect(url_for("change", number=d, pword=e))


    return render_template('delete.html', form1=form1, title=r)

@app.route("/change/<int:number>/<pword>", methods=["GET", "POST"])
def change(number, pword):
    form=Review()
    review = Reviews.query.filter_by(Review_ID=number).first()
    if request.method =="POST":
        review.Review_title=form.Review_title.data
        review.Reviewer_name=form.Reviewer_name.data
        review.Review_password=form.Review_password.data
        review.Review=form.Review.data
        review.Rating= form.Rating.data
        db.session.commit()
        return redirect(url_for("game", Title=review.Games_title))
    return render_template("change.html", form=form, title="Update", review=review)
    
