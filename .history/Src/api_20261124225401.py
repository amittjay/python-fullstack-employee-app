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
        # Audit - Kaun login hua
        add_audit(row[1], row[4], "LOGIN", f"{row[1]} ne login kiya")
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
@token_required  # Bina Token ke data nahi milega
def employees_api():
    # Role nikalo - Token se aaya hai
    user_role = request.user.get("role")
    username = request.user.get("username")

    conn = get_connection()
    cursor = conn.cursor()

    if request.method == "GET":
        # Soft Delete wala filter - Jo delete huye wo mat dikhao
        cursor.execute("SELECT id, name, city, experience, ctc FROM employees WHERE is_deleted = 0 OR is_deleted IS NULL")
        rows = cursor.fetchall()
        conn.close()
        data = [{"id": r[0], "name": r[1], "city": r[2], "experience": r[3], "ctc": r[4]} for r in rows]
        return jsonify(data)

    if request.method == "POST":
        # Sirf Admin aur HR hi Add kar sakte hai, Manager nahi
        if user_role not in ["Admin", "HR"]:
            return jsonify({"message": "Tumko Add Karne Ka Permission Nahi Hai - Sirf Admin/HR"}), 403
        data = request.json
        cursor.execute("INSERT INTO employees (name, city, experience, ctc) VALUES (?, ?, ?, ?)",
                       (data.get("name"), data.get("city"), int(data.get("experience") or 0), int(data.get("ctc") or 0)))
        conn.commit()
        conn.close()
        # Audit - Kisne add kiya
        add_audit(username, user_role, "ADD", f"{username} ne {data.get('name')} ko add kiya - CTC {data.get('ctc')} LPA")
        return jsonify({"message": "Employee SQL Server Me Save Ho Gaya!"})

@app.route("/employees/<int:emp_id>", methods=["DELETE"])
@token_required
def delete_api(emp_id):
    user_role = request.user.get("role")
    username = request.user.get("username")
    # Sirf Admin hi Delete kar sakta hai - Manager/HR nahi
    if user_role != "Admin":
        return jsonify({"message": "Sirf Admin Delete Kar Sakta Hai"}), 403

    conn = get_connection()
    cursor = conn.cursor()
    # Pehle naam nikaalo audit ke liye
    cursor.execute("SELECT name FROM employees WHERE id=?", (emp_id,))
    row = cursor.fetchone()
    emp_name = row[0] if row else f"ID {emp_id}"
    # Sach me delete nahi - Sirf is_deleted = 1 karo - Soft Delete
    cursor.execute("UPDATE employees SET is_deleted=1, deleted_at=GETDATE() WHERE id=?", (emp_id,))
    conn.commit()
    conn.close()
    # Audit - Kisne delete kiya
    add_audit(username, user_role, "DELETE", f"{username} ne {emp_name} (ID {emp_id}) ko delete kiya")
    return jsonify({"message": "Delete Ho Gaya! (Soft Delete - Data abhi bhi SQL me hai)"})

# NAYA - Audit Log dekhne ka API - Sirf Admin dekh sakta hai
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