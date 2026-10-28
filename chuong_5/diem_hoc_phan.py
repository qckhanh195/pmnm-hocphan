from flask import Flask, render_template, request

app = Flask(__name__)

def validate_score(val_str):
    """
    Hàm dùng chung để xử lý và kiểm tra dữ liệu điểm cho cả 3 ô:
    - Kiểm tra bỏ trống.
    - Thay thế dấu phẩy (,) thành dấu chấm (.).
    - Ép kiểu float và kiểm tra miền giá trị từ 0 đến 10.
    """
    if not val_str or val_str.strip() == "":
        return None, "Vui lòng nhập điểm."
    
    # Chuyển dấu phẩy thành dấu chấm
    clean_str = val_str.strip().replace(',', '.')
    
    try:
        val = float(clean_str)
        if val < 0 or val > 10:
            return None, "Điểm phải nằm trong khoảng từ 0 đến 10."
        return val, None
    except ValueError:
        return None, "Điểm nhập vào không hợp lệ."

@app.route('/', methods=['GET', 'POST'])
def index():
    cc_raw = ''
    gk_raw = ''
    ck_raw = ''
    result = None
    errors = {'cc': None, 'gk': None, 'ck': None}

    if request.method == 'POST':
        # Lấy dữ liệu từ form
        cc_raw = request.form.get('cc', '')
        gk_raw = request.form.get('gk', '')
        ck_raw = request.form.get('ck', '')

        # Gọi duy nhất 1 hàm validate_score cho cả 3 ô điểm
        cc_val, errors['cc'] = validate_score(cc_raw)
        gk_val, errors['gk'] = validate_score(gk_raw)
        ck_val, errors['ck'] = validate_score(ck_raw)

        # Nếu cả 3 ô đều hợp lệ (không có lỗi)
        if not errors['cc'] and not errors['gk'] and not errors['ck']:
            # Tính điểm học phần (Chuyên cần 10%, Giữa kỳ 30%, Cuối kỳ 60%)
            total_score = cc_val * 0.10 + gk_val * 0.30 + ck_val * 0.60
            
            # Làm tròn 1 chữ số thập phân
            total_score = round(total_score, 1)

            # Quy đổi điểm chữ (Cuối kỳ < 1 là bị điểm liệt -> F)
            if ck_val < 1:
                grade = 'F'
                note = "Bị điểm liệt môn học (Cuối kỳ < 1)"
            elif total_score >= 8.5:
                grade = 'A'
                note = "Đạt"
            elif total_score >= 7.0:
                grade = 'B'
                note = "Đạt"
            elif total_score >= 5.5:
                grade = 'C'
                note = "Đạt"
            elif total_score >= 4.0:
                grade = 'D'
                note = "Đạt"
            else:
                grade = 'F'
                note = "Kém (Khen/Không đạt)"

            result = {
                'score': total_score,
                'grade': grade,
                'note': note
            }

    return render_template(
        'diem_hoc_phan.html',
        cc=cc_raw,
        gk=gk_raw,
        ck=ck_raw,
        errors=errors,
        result=result
    )

if __name__ == '__main__':
    app.run(debug=True)