from flask import Flask, render_template, request, redirect, url_for, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
import jwt
import datetime
from functools import wraps

app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///books.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET KEY'] = 'thisisthesecretkey'
db = SQLAlchemy(app)


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    author = db.Column(db.String(250), nullable=False)
    rating = db.Column(db.Float, nullable=False)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(250), unique=True, nullable=False)
    password = db.Column(db.String(250), nullable=False)
    token = db.Column(db.String, nullable=False)


db.create_all()


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.args.get('token')
        if not token:
            return jsonify({"message": "Token is missing!"}), 403

        try:
            data = jwt.decode(token, app.config['SECRET KEY'])
        except:
            return jsonify({"message": "Token is invalid!"}), 403

        return f(*args, **kwargs)
    return decorated

@app.route('/unprotected')
def unprotected():
    return jsonify({"message":"Anyone can view this"})


@app.route('/protected')
@token_required
def protected():
    return jsonify({"message": "This is only available for people with valid tokens."})


@app.route('/login')
def login():
    auth = request.authorization
    if auth and auth.password == 'password':
        token = jwt.encode({"user": auth.username, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app.config['SECRET KEY'])
        return jsonify({"token": token})

    return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required"'})


@app.route('/')
def home():

    all_books = db.session.query(Book).all()
    return render_template("index.html", books=all_books)


@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":

        new_book = Book(
            title=request.form["title"],
            author=request.form["author"],
            rating=request.form["rating"]
        )
        db.session.add(new_book)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template("add.html")


@app.route("/edit", methods=["GET", "POST"])
def edit():
    if request.method == "POST":
        book_id = request.form["id"]
        book_to_update = Book.query.get(book_id)
        book_to_update.rating = request.form["rating"]
        db.session.commit()
        return redirect(url_for('home'))
    book_id = request.args.get('id')
    book_selected = Book.query.get(book_id)
    return render_template("edit_rating.html", book=book_selected)


@app.route("/delete")
def delete():
    book_id = request.args.get('id')
    book_to_delete = Book.query.get(book_id)
    db.session.delete(book_to_delete)
    db.session.commit()
    return redirect(url_for('home'))


if __name__ == "__main__":
    app.run(debug=True)
