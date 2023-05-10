from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


db = SQLAlchemy()
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///books.db"
db.init_app(app)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name_author = db.Column(db.String, unique=False, nullable=False)
    title = db.Column(db.String, unique=True, nullable=False)
    description = db.Column(db.String, unique=True, nullable=False)
    count = db.Column(db.Integer)
    price = db.Column(db.Integer)
    date = db.Column(db.DateTime, default=datetime.utcnow)

with app.app_context():
    db.create_all()


@app.route("/create", methods=["GET", "POST"])
def book_create():
    if request.method == "POST":
        book = Book(
            name_author = request.form['name_author'],
            title = request.form['title'],
            description = request.form['description'],
            count = request.form['count'],
            price = request.form['price']
        )
        try:
            db.session.add(book)
            db.session.commit()
            return redirect('/books')
        except:
            return 'При добавлении книги произошла ошибка'
    return render_template("create.html")

@app.route("/books")
def book_list():
    books = db.session.execute(db.select(Book).order_by(Book.name_author)).scalars()
    return render_template("book.html", books=books)

@app.route("/book/<int:id>")
def book_detail(id):
    book = db.get_or_404(Book, id)
    return render_template("detail.html", book=book)


@app.route("/book/<int:id>/delete", methods=["GET", "POST"])
def book_delete(id):
    book = db.get_or_404(Book, id)
    try:
        db.session.delete(book)
        db.session.commit()
        return redirect('/books')
    except:
        return "При удалении книги произошла ошибка"


@app.route("/book/<int:id>/update", methods=["GET", "POST"])
def book_update(id):
    book = db.get_or_404(Book, id)
    if request.method == "POST":
            book.name_author = request.form['name_author']
            book.title = request.form['title']
            book.description = request.form['description']
            book.count = request.form['count']
            book.price = request.form['price']

            try:
                db.session.commit()
                return redirect('/books')
            except:
                return 'При редактировании книги произошла ошибка'
            
    return render_template("update.html", book=book)


if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port='4400'
    )