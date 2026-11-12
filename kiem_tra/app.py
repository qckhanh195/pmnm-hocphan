from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, ForeignKey, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///library.db"
db.init_app(app)


class Category(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    books: Mapped[list["Book"]] = relationship(
        back_populates="category", cascade="all, delete-orphan"
    )


class Book(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    author: Mapped[str] = mapped_column(String(100), nullable=False)
    price: Mapped[int] = mapped_column(default=0)
    category_id: Mapped[int] = mapped_column(ForeignKey("category.id"), nullable=False)

    category: Mapped["Category"] = relationship(back_populates="books")


with app.app_context():
    db.create_all()


@app.route("/")
def index():
    category_id = request.args.get("category_id", type=int)
    total_categories = db.session.scalar(db.select(func.count(Category.id))) or 0
    total_books = db.session.scalar(db.select(func.count(Book.id))) or 0
    categories = db.session.scalars(db.select(Category).order_by(Category.id.desc())).all()

    book_query = db.select(Book).order_by(Book.id.desc())
    if category_id:
        book_query = book_query.where(Book.category_id == category_id)
    books = db.session.scalars(book_query).all()

    return render_template(
        "index.html",
        categories=categories,
        books=books,
        total_categories=total_categories,
        total_books=total_books,
        selected_category_id=category_id,
    )


@app.route("/categories/add", methods=["POST"])
def add_category():
    name = request.form.get("name", "").strip()
    if name:
        exists = db.session.scalar(db.select(Category).where(Category.name == name))
        if not exists:
            db.session.add(Category(name=name))
            db.session.commit()
    return redirect(url_for("index"))


@app.route("/categories/edit/<int:id>", methods=["GET", "POST"])
def edit_category(id):
    category = db.get_or_404(Category, id)
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        if name:
            exists = db.session.scalar(
                db.select(Category).where(Category.name == name, Category.id != id)
            )
            if not exists:
                category.name = name
                db.session.commit()
        return redirect(url_for("index"))
    return render_template("edit_category.html", category=category)


@app.route("/categories/delete/<int:id>", methods=["POST"])
def delete_category(id):
    category = db.get_or_404(Category, id)
    db.session.delete(category)
    db.session.commit()
    return redirect(url_for("index"))


@app.route("/books/add", methods=["POST"])
def add_book():
    title = request.form.get("title", "").strip()
    author = request.form.get("author", "").strip()
    price = request.form.get("price", type=int) or 0
    category_id = request.form.get("category_id", type=int)

    if title and author and category_id:
        new_book = Book(
            title=title,
            author=author,
            price=price,
            category_id=category_id,
        )
        db.session.add(new_book)
        db.session.commit()
    return redirect(url_for("index"))


@app.route("/books/edit/<int:id>", methods=["GET", "POST"])
def edit_book(id):
    book = db.get_or_404(Book, id)
    categories = db.session.scalars(db.select(Category)).all()

    if request.method == "POST":
        title = request.form.get("title", "").strip()
        author = request.form.get("author", "").strip()
        price = request.form.get("price", type=int) or 0
        category_id = request.form.get("category_id", type=int)
        if title and author and category_id:
            book.title = title
            book.author = author
            book.price = price
            book.category_id = category_id
            db.session.commit()
            return redirect(url_for("index"))

    return render_template("edit_book.html", book=book, categories=categories)


@app.route("/books/delete/<int:id>", methods=["POST"])
def delete_book(id):
    book = db.get_or_404(Book, id)
    db.session.delete(book)
    db.session.commit()
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)