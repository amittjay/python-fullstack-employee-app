from flask import Flask, jsonify, request
from flask_cors import CORS
from employee import Employee, employees_list, add_employee

app = Flask(__name__)
CORS(app)

# Pehle se 2 employee
emp1 = Employee(name="Amit Kumar Tiwari", city="New Delhi", experience=8, ctc=15)
emp2 = Employee(name=" 【entity-Rahul Sharma¦canonical_name=Rahul Sharma】", city="Lucknow", experience=2, ctc=8)
add_employee(emp1)
add_employee(emp2)

@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "API Chal Rahi Hai - /employees pe jao"})

# GET + POST - Dono ek hi jagah, taaki 405 na aaye
@app.route("/employees", methods=["GET", "POST"])
def employees_api():
    # Agar GET hai to List bhejo
    if request.method == "GET":
        data = []
        for emp in employees_list:
            data.append({
                "name": emp.name,
                "city": emp.city,
                "experience": emp.experience,
                "ctc": emp.ctc
            })
        return jsonify(data)

    # Agar POST hai to Naya Jodo
    if request.method == "POST":
        data = request.json
        naya_emp = Employee(
            name=data.get("name"),
            city=data.get("city"),
            experience=int(data.get("experience")),
            ctc=int(data.get("ctc"))
        )
        add_employee(naya_emp)
        return jsonify({"message": "Employee Jud Gaya!", "name": naya_emp.name})

@app.route("/search", methods=["GET"])
def search_api():
    naam = request.args.get("naam")
    for emp in employees_list:
        if emp.name.lower() == naam.lower():
            return jsonify({"name": emp.name, "city": emp.city, "experience": emp.experience, "ctc": emp.ctc})
    return jsonify({"message": "Nahi Mila"})

# GET + POST - Dono ek hi jagah
@app.route("/employees", methods=["GET", "POST"])
def employees_api():
    if request.method == "GET":
        data = []
        for emp in employees_list:
            data.append({
                "name": emp.name,
                "city": emp.city,
                "experience": emp.experience,
                "ctc": emp.ctc
            })
        return jsonify(data)

    if request.method == "POST":
        try:
            data = request.json
            print("POST Data Aaya:", data)  # Terminal me dikhega kya aaya

            # Khaali hai to 0 kar do, crash nahi hoga
            naam = data.get("name") or "Naam Nahi Hai"
            city = data.get("city") or "Delhi"
            exp = data.get("experience") or 0
            ctc = data.get("ctc") or 0

            naya_emp = Employee(
                name=naam,
                city=city,
                experience=int(exp),
                ctc=int(ctc)
            )
            add_employee(naya_emp)
            return jsonify({"message": "Employee Jud Gaya!", "name": naya_emp.name})
        except Exception as e:
            print("POST Error:", e)
            return jsonify({"message": f"Error: {e}"}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)