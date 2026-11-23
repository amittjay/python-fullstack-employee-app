import employee


class Employee:
    def __init__(self, name: str, city: str, experience: int, ctc: int):
        self.name = name
        self.city = city
        self.experience = experience
        self.ctc = ctc

    def get_info(self) -> str:
        return f"{self.name} - {self.city} - {self.experience} saal exp - {self.ctc} LPA"

    employees = []

def add_employee(emp):
    employee.append(emp)
    print(f"Employee Jud Gaya: {emp.name}")

    # Employee list - Database jaisa
employees_list = []

def add_employee(emp):
    employees_list.append(emp)
    print(f"Employee Jud Gaya: {emp.name}")

def search_employee(naam):
    # List me ek-ek karke dhoondo
    for emp in employees_list:
        if emp.name.lower() == naam.lower():
            print(f"Mil Gaya: {emp.get_info()}")
            return emp
    
    print(f"{naam} naam ka koi employee nahi mila")
    return None

def check_level(emp):
    # If-Else - Senior hai ya Junior
    if emp.experience >= 5:
        print(f"{emp.name} - Senior Developer Hai")
    else:
        print(f"{emp.name} - Junior Developer Hai")