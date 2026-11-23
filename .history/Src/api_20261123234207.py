# API - Python ka Dukaan
# React yahi se data maangega

from flask import Flask, jsonify, request
from flask_cors import CORS
from employee import Employee, employees_list, add_employee, search_employee

app = Flask(__name__)
@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "API Chal Rahi Hai - /employees pe jao"})

# Pehle se 2 employee daal diye - jaise Database me hote hai
emp1 = Employee(name="Amit Kumar Tiwari", city="New Delhi", experience=8, ctc=15)
emp2 = Employee(name=" 【entity-Rahul Sharma¦canonical_name=Rahul Sharma】", city="Lucknow", experience=2, ctc=8)
add_employee(emp1)
add_employee(emp2)

# 1. Sab Employee Dikhane Wala API
@app.route("/employees", methods=["GET"])
def get_employees():
    # List ko JSON me badal ke bhejo
    data = []
    for emp in employees_list:
        data.append({
            "name": emp.name,
            "city": emp.city,
            "experience": emp.experience,
            "ctc": emp.ctc
        })
    return jsonify(data)

# 2. Search Wala API
@app.route("/search", methods=["GET"])
def search_api():
    naam = request.args.get("naam")
    for emp in employees_list:
        if emp.name.lower() == naam.lower():
            return jsonify({"name": emp.name, "city": emp.city, "experience": emp.experience, "ctc": emp.ctc})
    return jsonify({"message": "Nahi Mila"})

# 3. Login Wala API - JWT wala yaad hai?
@app.route("/login", methods=["POST"])
def login_api():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if username == "amit" and password == "12345":
        return jsonify({"message": "Login Successful", "token": "jwt-token-12345"})
    else:
        return jsonify({"message": "Galat Password"})

if __name__ == "__main__":
    app.run(debug=True, port=5000)