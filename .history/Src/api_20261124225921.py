from flask import Flask, jsonify, request
from flask_cors import CORS
from database import get_connection
import jwt
import bcrypt
import datetime
from functools import wraps

app = Flask(__name__)
CORS(app)

# Secret Key - C# me appsettings.json me hoti thi
SECRET_KEY = "mera-super-secret-key-2026-employee-app"

# Token Check Karne Wala - Har API pe lagega
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get("Authorization")
        if not token:
            return jsonify({"message": "Token Nahi Hai - Pehle Login Karo"}), 401
        try:
            # Token se data nikalo - "Bearer TOKEN" me se TOKEN nikalo
            if token.startswith("Bearer "):
                token = token[7:]
            data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            request.user = data  # Aage ke liye save kar lo
        except jwt.ExpiredSignatureError:
            return jsonify({"message": "Token Expire Ho Gaya - Dobara Login Karo"}), 401
        except:
            return jsonify({"message": "Galat Token"}), 401
        return f(*args, **kwargs)
    return decorated

@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "API Chal Rahi Hai - Corporate Level"})

def add_audit(username, role, action, detail):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO audit_log (username, role, action, detail) VALUES (?, ?, ?, ?)",
                       (username, role, action, detail))
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

    # Password Check - Hash se compare karo
    stored_hash = row[2]
    if bcrypt.checkpw(password.encode('utf-8'), stored_hash.encode('utf-8')):
        # Real JWT Banao - Usme username, role, expiry hai
        token_data = {
            "username": row[1],
            "naam": row[3],
            "role": row[4],
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=2)  # 2 ghante me expire
        }
        token = jwt.encode(token_data, SECRET_KEY, algorithm="HS256")
        return jsonify({
            "message": "Login Successful",
            "token": token,
            "naam": row[3],
            "role": row[4],
            "username": row[1]
        })
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
        # Pagination + Filter + Sorting - URL se aayega
        # Example: /employees?page=1&limit=10&city=Noida&sort=ctc&order=desc&search=Priya
        page = int(request.args.get("page", 1))
        limit = int(request.args.get("limit", 10))
        city = request.args.get("city", "")
        search_q = request.args.get("search", "")
        sort_by = request.args.get("sort", "id")  # id, name, ctc, experience
        order = request.args.get("order", "asc")
        offset = (page - 1) * limit

        # Sorting ko safe rakho - SQL Injection se bacho
        allowed_sort = {"id": "id", "name": "name", "ctc": "ctc", "experience": "experience", "city": "city"}
        sort_col = allowed_sort.get(sort_by, "id")
        sort_dir = "DESC" if order == "desc" else "ASC"

        # WHERE banayo
        where = "WHERE (is_deleted = 0 OR is_deleted IS NULL)"
        params = []
        if city:
            where += " AND city LIKE ?"
            params.append(f"%{city}%")
        if search_q:
            where += " AND (name LIKE ? OR city LIKE ?)"
            params.append(f"%{search_q}%")
            params.append(f"%{search_q}%")

        # Total count nikalo - Kitne page banenge
        cursor.execute(f"SELECT COUNT(*) FROM employees {where}", params)
        total = cursor.fetchone()[0]

        # Page wala data nikalo - OFFSET FETCH
        query = f"SELECT id, name, city, experience, ctc FROM employees {where} ORDER BY {sort_col} {sort_dir} OFFSET ? ROWS FETCH NEXT ? ROWS ONLY"
        cursor.execute(query, params + [offset, limit])
        rows = cursor.fetchall()
        conn.close()
        data = [{"id": r[0], "name": r[1], "city": r[2], "experience": r[3], "ctc": r[4]} for r in rows]
        return jsonify({"employees": data, "total": total, "page": page, "limit": limit, "total_pages": (total + limit - 1)//limit})
if __name__ == "__main__":
    app.run(debug=True, port=5000)