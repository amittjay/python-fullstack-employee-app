from employee import Employee, add_employee, search_employee, check_level
from salary import calculate_hike, calculate_monthly_salary

def main():
    # 3 Employee banao
    emp1 = Employee(name="Amit Kumar Tiwari", city="New Delhi", experience=8, ctc=15)
    emp2 = Employee(name="【entity-Rahul Sharma¦canonical_name=Rahul Sharma】", city="Lucknow", experience=2, ctc=8)
    emp3 = Employee(name="Priya Singh", city="Noida", experience=6, ctc=12)

    # List me jodo
    add_employee(emp1)
    add_employee(emp2)
    add_employee(emp3)

    print("\n--- Senior / Junior Check ---")
    check_level(emp1)
    check_level(emp2)

    print("\n--- Search Karo ---")
    search_employee("【entity-Rahul Sharma¦canonical_name=Rahul Sharma】")
    search_employee("Amit Kumar Tiwari")
    search_employee("Koi Nahi Hai")

    # Salary wala purana kaam
    new_ctc = calculate_hike(emp1.ctc, 30)
    print(f"\nAmit ka Naya CTC: {new_ctc} LPA")

if __name__ == "__main__":
    main()