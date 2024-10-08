import Controller


class User:
    
    def __init__(self, username, password, homeDir):
        self.username = username
        self.password = password
        self.homedir = homeDir
    
    def addUser(self):
        Controller.createUser(self.username, self.password, self.homedir)
                

    def print_user(self):
        print(f"Name: {self.name}, Age: {self.age}")