from employee import Employee
from salary import calculate_hike, calculate_monthly_salary

def main():
    emp = Employee(
        name="Amit Kumar Tiwari",
        age=30,
        po
        ctc=15
    )

    print(emp.get_info())

    new_ctc = calculate_hike(emp.ctc, 30)
    monthly = calculate_monthly_salary(new_ctc)

    print(f"30% Hike ke baad Naya CTC: {new_ctc} LPA")
    print(f"Monthly Salary: Rs. {monthly}")

if __name__ == "__main__":
    main()