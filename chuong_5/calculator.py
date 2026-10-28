from flask import Flask, render_template, request

app = Flask(__name__)

def parse_number(val_str):
    if not val_str or val_str.strip() == "":
        return None, "Vui lòng nhập số."
    
    clean_str = val_str.strip().replace(',', '.')
    
    try:
        val = float(clean_str)
        return val, None
    except ValueError:
        return None, "Giá trị nhập vào không phải là số hợp lệ."

def format_number(num):
    return int(num) if num.is_integer() else num

@app.route('/', methods=['GET', 'POST'])
def index():
    a_raw = ''
    b_raw = ''
    op = '+'
    result = None
    errors = {'a': None, 'b': None, 'op': None}

    if request.method == 'POST':
        # Lấy dữ liệu từ form bằng request.form
        a_raw = request.form.get('a', '')
        b_raw = request.form.get('b', '')
        op = request.form.get('op', '+')

        a_val, err_a = parse_number(a_raw)
        if err_a:
            errors['a'] = err_a

        b_val, err_b = parse_number(b_raw)
        if err_b:
            errors['b'] = err_b

        valid_ops = ['+', '-', '*', '/']
        if op not in valid_ops:
            errors['op'] = "Phép toán không hợp lệ."

        if not errors['a'] and not errors['b'] and not errors['op']:
            if op == '/' and b_val == 0:
                errors['b'] = "Không thể chia cho số 0."
            else:
                if op == '+':
                    res = a_val + b_val
                elif op == '-':
                    res = a_val - b_val
                elif op == '*':
                    res = a_val * b_val
                elif op == '/':
                    res = a_val / b_val

                a_disp = format_number(a_val)
                b_disp = format_number(b_val)
                res_disp = format_number(res)

                result = f"{a_disp} {op} {b_disp} = {res_disp}"

    return render_template(
        'calculator.html',
        a=a_raw,
        b=b_raw,
        op=op,
        errors=errors,
        result=result
    )

if __name__ == '__main__':
    app.run(debug=True)