#!/usr/bin/env python3

from flask import Flask, request, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from models import db, User, Review, Game

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

@app.route('/')
def index():
    return "Index for Game/Review/User API"

@app.route('/games')
def games():
    games = [ 
        {
            "title": game.title,
            "genre": game.genre,
            "platform": game.platform,
            "price": game.price,
        }
        for game in Game.query.all()
    ]

    return make_response(games, 200)

@app.route('/games/<int:id>')
def game_by_id(id):
    game = Game.query.filter(Game.id == id).first()

    if not game:
        return make_response({"error": "Game not found"}, 404)

    return make_response(game.to_dict(), 200)

@app.route('/users')
def users():
    users = [user.to_dict() for user in User.query.all()]
    return make_response(users, 200)

@app.route('/reviews', methods=['GET', 'POST'])
def handle_reviews():
    if request.method == 'GET':
        reviews = [review.to_dict() for review in Review.query.all()]
        return make_response(reviews, 200)

    elif request.method == 'POST':
        try:
            new_review = Review(
                score=request.form.get("score"),
                comment=request.form.get("comment"),
                game_id=request.form.get("game_id"),
                user_id=request.form.get("user_id")
            )
            db.session.add(new_review)
            db.session.commit()

            return make_response(new_review.to_dict(), 201)
        except Exception as e:
            return make_response({"error": str(e)}, 400)

@app.route('/reviews/<int:id>', methods=['GET', 'DELETE'])
def review_by_id(id):
    review = Review.query.filter_by(id=id).first()

    if not review:
        return make_response({"error": "Review not found"}, 404)

    if request.method == 'GET':
        return make_response(review.to_dict(), 200)

    elif request.method == 'DELETE':
        db.session.delete(review)
        db.session.commit()
        return make_response({
            "delete_successful": True,
            "message": "Review deleted."
        }, 200)
    elif request.method == 'DELETE':
            db.session.delete(review)
            db.session.commit()

            response_body = {
                "delete_successful": True,
                "message": "Review deleted."
            }

            response = make_response(
                response_body,
                200
            )

            return response

if __name__ == '__main__':
    app.run(port=5555, debug=True)
