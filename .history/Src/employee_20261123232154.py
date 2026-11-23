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