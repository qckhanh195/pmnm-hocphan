from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    a = request.form.get('a')
    b = request.form.get('b')
    if a is None:
        a = 0
    if b is None:
        b = 0
    a = float(a)
    b = float(b)
    chia = a / b if b != 0 else 0
    return render_template("math.html", a = a, b = b, cong = a + b, tru = a - b, nhan = a * b, chia = chia)

if __name__ == "__main__":
    app.run(debug=True)