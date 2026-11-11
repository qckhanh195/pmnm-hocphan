from flask import Flask, render_template
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
      Student(mssv="23T1020002", name="Trần Thị B", gpa=7.5),
      Student(mssv="23T1020003", name="Lê Hoàng C", gpa=9.0),
      Student(mssv="23T1020004", name="Phạm Minh D", gpa=6.8),
      Student(mssv="23T1020005", name="Nguyễn Thị E", gpa=8.2),
    ])
    db.session.commit()
    return (f"Đã thêm 5 sinh viên. id của An: "
            f"trước commit = {before}, "
            f"sau commit = {an.id}")

@app.get("/thu-truy-van")
def try_queries():
    if db.session.scalar(db.select(func.count(Student.id))) == 0:
        return "Chưa có dữ liệu, hãy mở /them-mau trước."
    
    lines = []
    lines.append(f"1. get(3) : {db.session.get(Student, 3)}")
    lines.append(f"2. get(99) : {db.session.get(Student, 99)}")
    
    everyone = db.session.scalars(db.select(Student)).all()
    lines.append(f"3. Tất cả: {everyone} sinh viên")
    
    stat = db.select(Student).where(Student.gpa >= 8).order_by(Student.gpa.desc())
    good = db.session.scalars(stat).all()
    lines.append(f"4. Điểm (GPA >= 8): {good}")
    
    binh = db.session.scalar(db.select(Student).filter_by(mssv="23T1020002"))
    lines.append(f"5. MSSV 23T10202002: {binh}")
    
    total = db.session.scalar(db.select(func.count(Student.id)))
    avg_gpa = db.session.scalar(db.select(func.avg(Student.gpa)))
    lines.append(f"6. Số sinh viên: {total}, Điểm trung bình: {avg_gpa:.2f}")
    
    return render_template("try_queries.html", lines=lines, everyone=everyone)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)