from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    pass

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///qlsv.db"

db = SQLAlchemy(app, model_class=Base)

class Student(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    mssv: Mapped[str] = mapped_column(String(10), unique=True)
    name: Mapped[str] = mapped_column(String(100))
    gpa: Mapped[float] = mapped_column(default=0.0)

    def __repr__(self) -> str:
        return f"<Student {self.mssv} - {self.name}>"

@app.get("/them-mau")
def add_sample():
    total= db.session.scalar(
      db.select(func.count(Student.id)))
    if total > 0:
      return f"Đã có {total} sinh viên, không thêm nữa."
    an = Student(mssv="23T1020001", name="Nguyễn Văn A", gpa=8.5)
    before = an.id
    db.session.add(an)
    db.session.add_all([
      Student(mssv="23T1020002", name="Trần Thị Bình", gpa=7.5),
      Student(mssv="23T1020003", name="Lê Hoàng C", gpa=9.0),
      Student(mssv="23T1020004", name="Phạm Minh D", gpa=6.8),
      Student(mssv="23T1020005", name="Nguyễn Thị E", gpa=8.2),
    ])
    db.session.commit()
    return (f"Đã thêm 5 sinh viên. id của An: "
            f"trước commit = {before}, "
            f"sau commit = {an.id}")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)