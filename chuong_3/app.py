from flask import Flask, request as req, url_for
app = Flask(__name__)

@app.route('/')
@app.route('/index')
@app.route('/home')
def index():
  return f'<a href="">Trang chủ</a> <hr> <a href="{url_for("gioi_thieu")}">Giới thiệu</a>'

@app.route('/gioi-thieu')
@app.route('/about')
def gioi_thieu():
  return 'Gioi thieu'

@app.route('/user/<username>')
def user_profile(username):
  return f'Xin chao, {username}!'

@app.route('/square/<float:x>')
def square(x):
  return f'gia tri binh phuong cua {x} la: {x**2}'

@app.route('/square2/<x>')
def square2(x):
  return f'gia tri binh phuong cua {float(x)} la: {float(x)**2}'

@app.route('/sum/<strs>')
def tong(strs):
  numbers = strs.split(',')
  total = sum(float(num) for num in numbers)
  return f'Tong cua {strs} la: {total}'

@app.route('/tinh-toan')
def tinh_toan():
  a = req.args.get('a', float)
  b = req.args.get('b', float)
  op = req.args.get('op')
  if a is None or b is None or op is None:
    return 'truyen thieu'
  if op == 'add':
    return f'{a} + {b} = {a + b}'
  elif op == 'sub':
    return f'{a} - {b} = {float(a) - float(b)}'
  else:
    return 'truyen sai tham so'

POSTS = [
  {
    "id": 1,
    "title": "Chào Flask",
    "author": "an",
    "content": "Flask là một micro-framework...",
    "created": "2026-09-01",
  },
]

@app.route('/find-post/<int:post_id>')
def find_post(post_id):
  for post in POSTS:
    if post['id'] == post_id:
      return post
  return None

if __name__ == '__main__':
  app.run(debug=True)