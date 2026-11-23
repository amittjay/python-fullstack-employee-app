class mployee():
    def __init__(self, name, age, position):
        self.name = name
        self.age = age
        self.position = position

    def get_info(self):
        print(f"Name: {self.name}, Age: {self.age}, Position: {self.position}")