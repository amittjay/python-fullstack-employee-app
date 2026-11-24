from flask import Flask, jsonify, request
from flask_cors import CORS
from database import get_connection
import jwt
import bcrypt
import datetime
import re
from functools import wraps

app = Flask(__name__)
CORS(app)
SECRET_KEY = "mera-super-secret-key-2026-employee-app"

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get("Authorization")
        if not token:
            return jsonify({"message": "Token Nahi Hai - Pehle Login Karo"}), 401
        try:
            if token.startswith("Bearer "):
                token = token[7:]
            data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            request.user = data
        except jwt.ExpiredSignatureError:
            return jsonify({"message": "Token Expire Ho Gaya - Dobara Login Karo"}), 401
        except:
            return jsonify({"message": "Galat Token"}), 401
        return f(*args, **kwargs)
    return decorated

@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "API Chal Rahi Hai - Corporate Level + AI"})

def add_audit(username, role, action, detail):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO audit_log (username, role, action, detail) VALUES (?, ?, ?, ?)", (username, role, action, detail))
        conn.commit()
        conn.close()
    except Exception as e:
        print("Audit Error:", e)

@app.route("/login", methods=["POST"])
def login_api():
    data = request.json
    username = data.get("username")
    password = data.get("password")
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, username, password, naam, role FROM users WHERE username=?", (username,))
    row = cursor.fetchone()
    conn.close()
    if not row:
        return jsonify({"message": "User Nahi Mila"})
    stored_hash = row[2]
    if bcrypt.checkpw(password.encode('utf-8'), stored_hash.encode('utf-8')):
        add_audit(row[1], row[4], "LOGIN", f"{row[1]} ne login kiya")
        token_data = {"username": row[1], "naam": row[3], "role": row[4], "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=2)}
        token = jwt.encode(token_data, SECRET_KEY, algorithm="HS256")
        return jsonify({"message": "Login Successful", "token": token, "naam": row[3], "role": row[4], "username": row[1]})
    else:
        return jsonify({"message": "Galat Password"})

@app.route("/employees", methods=["GET", "POST"])
@token_required
def employees_api():
    user_role = request.user.get("role")
    username = request.user.get("username")
    conn = get_connection()
    cursor = conn.cursor()
    if request.method == "GET":
        page = int(request.args.get("page", 1))
        limit = int(request.args.get("limit", 10))
        city = request.args.get("city", "")
        search_q = request.args.get("search", "")
        sort_by = request.args.get("sort", "id")
        order = request.args.get("order", "asc")
        offset = (page - 1) * limit
        allowed_sort = {"id": "id", "name": "name", "ctc": "ctc", "experience": "experience", "city": "city"}
        sort_col = allowed_sort.get(sort_by, "id")
        sort_dir = "DESC" if order == "desc" else "ASC"
        where = "WHERE (is_deleted = 0 OR is_deleted IS NULL)"
        params = []
        if city:
            where += " AND city LIKE ?"
            params.append(f"%{city}%")
        if search_q:
            where += " AND (name LIKE ? OR city LIKE ?)"
            params.append(f"%{search_q}%")
            params.append(f"%{search_q}%")
        cursor.execute(f"SELECT COUNT(*) FROM employees {where}", params)
        total = cursor.fetchone()[0]
        query = f"SELECT id, name, city, experience, ctc FROM employees {where} ORDER BY {sort_col} {sort_dir} OFFSET ? ROWS FETCH NEXT ? ROWS ONLY"
        cursor.execute(query, params + [offset, limit])
        rows = cursor.fetchall()
        conn.close()
        data = [{"id": r[0], "name": r[1], "city": r[2], "experience": r[3], "ctc": r[4]} for r in rows]
        return jsonify({"employees": data, "total": total, "page": page, "limit": limit, "total_pages": (total + limit - 1)//limit})
    if request.method == "POST":
        if user_role not in ["Admin", "HR"]:
            return jsonify({"message": "Tumko Add Karne Ka Permission Nahi Hai - Sirf Admin/HR"}), 403
        data = request.json
        cursor.execute("INSERT INTO employees (name, city, experience, ctc) VALUES (?, ?, ?, ?)",
                       (data.get("name"), data.get("city"), int(data.get("experience") or 0), int(data.get("ctc") or 0)))
        conn.commit()
        conn.close()
        add_audit(username, user_role, "ADD", f"{username} ne {data.get('name')} ko add kiya - CTC {data.get('ctc')} LPA")
        return jsonify({"message": "Employee SQL Server Me Save Ho Gaya!"})

@app.route("/employees/bulk", methods=["POST"])
@token_required
def bulk_api():
    user_role = request.user.get("role")
    username = request.user.get("username")
    if user_role not in ["Admin", "HR"]:
        return jsonify({"message": "Sirf Admin/HR Bulk Upload Kar Sakte Hai"}), 403
    data = request.json
    emp_list = data.get("employees", [])
    if not emp_list:
        return jsonify({"message": "Koi Data Nahi Aaya"}), 400
    conn = get_connection()
    cursor = conn.cursor()
    count = 0
    for e in emp_list:
        try:
            name = (e.get("name") or "").strip()
            city = (e.get("city") or "").strip()
            if not name:
                continue
            cursor.execute("INSERT INTO employees (name, city, experience, ctc) VALUES (?, ?, ?, ?)",
                           (name, city, int(e.get("experience") or 0), int(e.get("ctc") or 0)))
            count += 1
        except:
            continue
    conn.commit()
    conn.close()
    add_audit(username, user_role, "BULK_UPLOAD", f"{username} ne {count} employee ek saath upload kiye - Excel/CSV se")
    return jsonify({"message": f"{count} Employee Upload Ho Gaye!"})

@app.route("/payroll/<int:emp_id>", methods=["GET"])
@token_required
def payroll_api(emp_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, city, experience, ctc FROM employees WHERE id=? AND (is_deleted=0 OR is_deleted IS NULL)", (emp_id,))
    row = cursor.fetchone()
    conn.close()
    if not row:
        return jsonify({"message": "Employee Nahi Mila"}), 404
    ctc_lpa = row[4] or 0
    annual = ctc_lpa * 100000
    monthly_ctc = round(annual / 12)
    basic = round(monthly_ctc * 0.40)
    hra = round(monthly_ctc * 0.20)
    pf = round(basic * 0.12)
    tax = round(monthly_ctc * 0.05) if monthly_ctc > 80000 else 0
    net = monthly_ctc - pf - tax
    return jsonify({"id": row[0], "name": row[1], "city": row[2], "experience": row[3], "ctc": ctc_lpa, "monthly_ctc": monthly_ctc, "basic": basic, "hra": hra, "pf": pf, "tax": tax, "net_salary": net})

# NAYA - AI SEARCH - Hindi / Hinglish / English me likho, samajh jayega
@app.route("/ai-search", methods=["GET"])
@token_required
def ai_search_api():
    q = (request.args.get("q", "") or "").lower()
    conn = get_connection()
    cursor = conn.cursor()
    where = "WHERE (is_deleted = 0 OR is_deleted IS NULL)"
    params = []
    explain = []

    # City nikaalo
    cities = ["noida","delhi","lucknow","bangalore","mumbai","pune","hyderabad","gurgaon","chennai","kolkata","indore","jaipur","ahmedabad","chandigarh","bhopal","patna","kanpur","varanasi","dehradun","allahabad"]
    for c in cities:
        if c in q:
            where += " AND city LIKE ?"
            params.append(f"%{c}%")
            explain.append(f"City = {c.capitalize()}")
            break

    # Experience - "5 saal se zyada", "5+ years", "5 saal se kam"
    m = re.search(r"(\d+)\s*(saal|year|yrs|exp)", q)
    if m:
        val = int(m.group(1))
        if "kam" in q or "less" in q or "se kam" in q or "<" in q:
            where += " AND experience < ?"
            explain.append(f"Experience < {val} saal")
        else:
            where += " AND experience >= ?"
            explain.append(f"Experience >= {val} saal")
        params.append(val)
    elif "senior" in q:
        where += " AND experience >= ?"
        params.append(5)
        explain.append("Senior = Exp >= 5 saal")
    elif "junior" in q or "fresher" in q:
        where += " AND experience < ?"
        params.append(5)
        explain.append("Junior = Exp < 5 saal")

    # CTC - "15 LPA se zyada", "20 se kam", "15+ ctc"
    m2 = re.search(r"(\d+)\s*(lpa|ctc|lakh|package)", q)
    if m2:
        val = int(m2.group(1))
        if "kam" in q or "less" in q or "se kam" in q:
            where += " AND ctc < ?"
            explain.append(f"CTC < {val} LPA")
        else:
            where += " AND ctc >= ?"
            explain.append(f"CTC >= {val} LPA")
        params.append(val)

    # Naam se search - agar koi city/exp/ctc nahi mila to naam maano
    if not explain:
        where += " AND (name LIKE ? OR city LIKE ?)"
        params.append(f"%{q}%")
        params.append(f"%{q}%")
        explain.append(f"Naam / City me '{q}' dhoondha")

    cursor.execute(f"SELECT TOP 50 id, name, city, experience, ctc FROM employees {where} ORDER BY ctc DESC", params)
    rows = cursor.fetchall()
    conn.close()
    data = [{"id": r[0], "name": r[1], "city": r[2], "experience": r[3], "ctc": r[4]} for r in rows]
    return jsonify({"employees": data, "total": len(data), "explain": " + ".join(explain), "query": q})

# NAYA - AI REPORT - Ek click me poori company ki report
@app.route("/ai-report", methods=["GET"])
@token_required
def ai_report_api():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*), AVG(CAST(ctc AS FLOAT)), AVG(CAST(experience AS FLOAT)), MAX(ctc), MIN(ctc) FROM employees WHERE (is_deleted=0 OR is_deleted IS NULL)")
    r = cursor.fetchone()
    total, avg_ctc, avg_exp, max_ctc, min_ctc = r[0] or 0, round(r[1] or 0, 1), round(r[2] or 0, 1), r[3] or 0, r[4] or 0
    cursor.execute("SELECT TOP 1 city, COUNT(*) as cnt FROM employees WHERE (is_deleted=0 OR is_deleted IS NULL) GROUP BY city ORDER BY cnt DESC")
    top_city_row = cursor.fetchone()
    top_city = top_city_row[0] if top_city_row else "N/A"
    top_city_count = top_city_row[1] if top_city_row else 0
    cursor.execute("SELECT TOP 3 name, city, experience, ctc FROM employees WHERE (is_deleted=0 OR is_deleted IS NULL) ORDER BY ctc DESC")
    top_earners = [{"name": x[0], "city": x[1], "experience": x[2], "ctc": x[3]} for x in cursor.fetchall()]
    cursor.execute("SELECT COUNT(*) FROM employees WHERE (is_deleted=0 OR is_deleted IS NULL) AND experience >= 5")
    senior = cursor.fetchone()[0]
    junior = total - senior
    cursor.execute("SELECT city, COUNT(*) as cnt, AVG(CAST(ctc AS FLOAT)) as avg_ctc FROM employees WHERE (is_deleted=0 OR is_deleted IS NULL) GROUP BY city ORDER BY cnt DESC")
    city_break = [{"city": x[0], "count": x[1], "avg_ctc": round(x[2] or 0, 1)} for x in cursor.fetchall()]
    conn.close()
    senior_pct = round((senior/total*100) if total else 0)
    lines = [
        f"📊 Total {total} Employee hai company me.",
        f"💰 Average CTC {avg_ctc} LPA hai, Average Experience {avg_exp} saal hai.",
        f"🏙️ Sabse zyada hiring {top_city} me hui hai — {top_city_count} log.",
        f"👑 Sabse zyada package {top_earners[0]['name'] if top_earners else 'N/A'} ka hai — {max_ctc} LPA ({top_earners[0]['city'] if top_earners else ''}).",
        f"📈 Team me {senior_pct}% Senior (5+ saal) aur {100-senior_pct}% Junior hai.",
        f"💡 Suggestion: {top_city} me hiring achhi chal rahi hai, waha aur focus karo. Junior ko train karke Senior banao to cost bachegi.",
    ]
    return jsonify({"total": total, "avg_ctc": avg_ctc, "avg_exp": avg_exp, "max_ctc": max_ctc, "min_ctc": min_ctc, "top_city": top_city, "top_city_count": top_city_count, "senior": senior, "junior": junior, "senior_pct": senior_pct, "top_earners": top_earners, "city_break": city_break, "summary_lines": lines})

@app.route("/employees/<int:emp_id>", methods=["DELETE"])
@token_required
def delete_api(emp_id):
    user_role = request.user.get("role")
    username = request.user.get("username")
    if user_role != "Admin":
        return jsonify({"message": "Sirf Admin Delete Kar Sakta Hai"}), 403
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM employees WHERE id=?", (emp_id,))
    row = cursor.fetchone()
    emp_name = row[0] if row else f"ID {emp_id}"
    cursor.execute("UPDATE employees SET is_deleted=1, deleted_at=GETDATE() WHERE id=?", (emp_id,))
    conn.commit()
    conn.close()
    add_audit(username, user_role, "DELETE", f"{username} ne {emp_name} (ID {emp_id}) ko delete kiya")
    return jsonify({"message": "Delete Ho Gaya! (Soft Delete - Data abhi bhi SQL me hai)"})

@app.route("/employees/<int:emp_id>", methods=["PUT"])
@token_required
def edit_api(emp_id):
    user_role = request.user.get("role")
    username = request.user.get("username")
    if user_role not in ["Admin", "HR"]:
        return jsonify({"message": "Sirf Admin/HR Edit Kar Sakte Hai"}), 403
    data = request.json
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM employees WHERE id=?", (emp_id,))
    row = cursor.fetchone()
    old_name = row[0] if row else f"ID {emp_id}"
    cursor.execute("UPDATE employees SET name=?, city=?, experience=?, ctc=? WHERE id=?",
                   (data.get("name"), data.get("city"), int(data.get("experience") or 0), int(data.get("ctc") or 0), emp_id))
    conn.commit()
    conn.close()
    add_audit(username, user_role, "EDIT", f"{username} ne {old_name} (ID {emp_id}) ko edit kiya - Naya: {data.get('name')}, {data.get('city')}, CTC {data.get('ctc')} LPA")
    return jsonify({"message": "Edit Ho Gaya!"})

@app.route("/audit", methods=["GET"])
@token_required
def audit_api():
    if request.user.get("role") != "Admin":
        return jsonify({"message": "Sirf Admin Audit Log dekh sakta hai"}), 403
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT TOP 50 username, role, action, detail, created_at FROM audit_log ORDER BY created_at DESC")
    rows = cursor.fetchall()
    conn.close()
    data = [{"username": r[0], "role": r[1], "action": r[2], "detail": r[3], "time": str(r[4])} for r in rows]
    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True, port=5000)