from employee import employee
from salary import calculate_hike, calculate_monthly_salary
def main():
    emp = employee( name="Amit Kumar Tiwari",
        city="New Delhi",
        experience=8,
        ctc=1500000,
        position="Software Engineer")
    print(emp.get_info())
    new_ctc = calculate_hike(emp.ctc, 30)
    monthly_salary = calculate_monthly_salary(new_ctc)
    print(f"New CTC: {new_ctc}")
    print(f"Monthly Salary: {monthly_salary}")
    if __name__ == "__main__":