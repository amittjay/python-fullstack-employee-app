from flask import Flask, jsonify, request
from flask_cors import CORS
from database import get_connection

app = Flask(__name__)
CORS(app)

@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "API Chal Rahi Hai - /employees pe jao"})

@app.route("/login", methods=["POST"])
def login_api():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    row = cursor.fetchone()
    conn.close()

    if row:
        # row[3] = naam (id=0, username=1, password=2, naam=3)
        return jsonify({"message": "Login Successful", "token": "jwt-token-12345", "naam": row[3]})
    else:
        return jsonify({"message": "Galat Password"})

@app.route("/employees", methods=["GET", "POST"])
def employees_api():
    conn = get_connection()
    cursor = conn.cursor()

    if request.method == "GET":
        cursor.execute("SELECT id, name, city, experience, ctc FROM employees")
        rows = cursor.fetchall()
        conn.close()
        # r[0]=id, r[1]=name, r[2]=city, r[3]=experience, r[4]=ctc
        data = [{"id": r[0], "name": r[1], "city": r[2], "experience": r[3], "ctc": r[4]} for r in rows]
        return jsonify(data)

    if request.method == "POST":
        data = request.json
        cursor.execute("INSERT INTO employees (name, city, experience, ctc) VALUES (?, ?, ?, ?)",
                       (data.get("name"), data.get("city"), int(data.get("experience") or 0), int(data.get("ctc") or 0)))
        conn.commit()
        conn.close()
        return jsonify({"message": "Employee SQL Server Me Save Ho Gaya!"})

@app.route("/employees/<int:emp_id>", methods=["DELETE"])
def delete_api(emp_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM employees WHERE id=?", (emp_id,))
    conn.commit()
    conn.close()
    return jsonify({"message": "Delete Ho Gaya!"})

if __name__ == "__main__":
    app.run(debug=True, port=5000)