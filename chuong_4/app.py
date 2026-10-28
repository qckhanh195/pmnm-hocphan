from datetime import datetime

from flask import Flask, render_template, request
app = Flask(__name__)

SHOP = {"name": "Cà phê sông Hương",
        "address": "12 Lê Lợi, Huế",
        "open": 7, "close": 22,
        "phone": "0234 567 890"}

PROMOTIONS = [
  "Giảm 10% cho sinh viên",
  "Mua 2 tặng 1 vào thứ Hai"]

MENU = [
    {"name": "cà phê đen", "price": 20000, "available": True},
    {"name": "bạc xỉu", "price": 30000, "available": False},
    {"name": "cà phê muối", "price": 25000, "available": True},
    {"name": "trà đào cam sả", "price": 35000, "available": True},
    {"name": "trà vải", "price": 30000, "available": True},
]

@app.get("/")
def index():
  hour = request.args.get("gio", type = int)
  if hour is None:
    hour = datetime.now().hour
  is_open = SHOP["open"] <= hour < SHOP["close"]
  return render_template("index.html", shop=SHOP,
    hour = hour, is_open = is_open,
    promotions = PROMOTIONS)

@app.get("/menu")
def menu_page():
   return render_template("menu.html", shop=SHOP, menu=MENU)

if __name__ == "__main__":
    app.run(debug=True)
