from flask import Flask, render_template, request

app = Flask(__name__)

def validate_input(val_str, min_val, max_val):
    if not val_str or val_str.strip() == "":
        return None, "Vui lòng nhập giá trị."
    
    clean_str = val_str.strip().replace(',', '.')
    
    try:
        val = float(clean_str)
        if val < min_val or val > max_val:
            return None, f"Giá trị phải từ {min_val} đến {max_val}."
        return val, None
    except ValueError:
        return None, "Dữ liệu nhập vào không hợp lệ."

@app.route('/', methods=['GET', 'POST'])
def index():
    height_raw = ''
    weight_raw = ''
    result = None
    errors = {'height': None, 'weight': None}

    if request.method == 'POST':
        height_raw = request.form.get('height', '')
        weight_raw = request.form.get('weight', '')

        # Gọi duy nhất 1 hàm validate_input cho cả 2 ô với khoảng giới hạn tương ứng
        height_cm, errors['height'] = validate_input(height_raw, 50, 250)
        weight_kg, errors['weight'] = validate_input(weight_raw, 10, 300)

        # Nếu dữ liệu cả 2 ô hợp lệ
        if not errors['height'] and not errors['weight']:
            # Đổi chiều cao từ cm sang mét
            height_m = height_cm / 100.0

            # Tính BMI = Cân nặng / (Chiều cao m)^2
            bmi = weight_kg / (height_m ** 2)
            bmi_rounded = round(bmi, 1)

            if bmi_rounded < 18.5:
                category = "Thiếu cân"
                color_class = "warning"  # Vàng
            elif bmi_rounded < 23.0:
                category = "Bình thường"
                color_class = "success"  # Xanh
            elif bmi_rounded < 25.0:
                category = "Thừa cân"
                color_class = "warning"  # Vàng
            else:
                category = "Béo phì"
                color_class = "danger"   # Đỏ

            # Tính khoảng cân nặng lý tưởng (BMI 18.5 - 22.9)
            min_ideal_weight = round(18.5 * (height_m ** 2), 1)
            max_ideal_weight = round(22.9 * (height_m ** 2), 1)

            result = {
                'bmi': bmi_rounded,
                'category': category,
                'color_class': color_class,
                'min_weight': min_ideal_weight,
                'max_weight': max_ideal_weight
            }

    return render_template(
        'bmi.html',
        height=height_raw,
        weight=weight_raw,
        errors=errors,
        result=result
    )

if __name__ == '__main__':
    app.run(debug=True)