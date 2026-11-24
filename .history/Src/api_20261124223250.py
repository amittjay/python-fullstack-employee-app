from flask import Flask, jsonify, request
from flask_cors import CORS
# from database import get_connection, init_db
from database import get_connection
app = Flask(__name__)
CORS(app)
# init_db()

@app.route("/login", methods=["POST"])
def login_api():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    conn = get_connection()
    user = conn.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password)).fetchone()
    conn.close()

    if user:
        # return jsonify({"message": "Login Successful", "token": "jwt-token-12345", "naam": user["naam"]})
    else:
        return jsonify({"message": "Galat Password"})

@app.route("/employees", methods=["GET", "POST"])
def employees_api():
    conn = get_connection()
    if request.method == "GET":
        rows = conn.execute("SELECT * FROM employees").fetchall()
        conn.close()
        data = [{"id": r["id"], "name": r["name"], "city": r["city"], "experience": r["experience"], "ctc": r["ctc"]} for r in rows]
        return jsonify(data)

    if request.method == "POST":
        data = request.json
        conn.execute("INSERT INTO employees (name, city, experience, ctc) VALUES (?, ?, ?, ?)",
                     (data.get("name"), data.get("city"), int(data.get("experience") or 0), int(data.get("ctc") or 0)))
        conn.commit()
        conn.close()
        return jsonify({"message": "Employee SQL Me Save Ho Gaya!"})

@app.route("/employees/<int:emp_id>", methods=["DELETE"])
def delete_api(emp_id):
    conn = get_connection()
    conn.execute("DELETE FROM employees WHERE id=?", (emp_id,))
    conn.commit()
    conn.close()
    return jsonify({"message": "Delete Ho Gaya!"})

if __name__ == "__main__":
    app.run(debug=True, port=5000)