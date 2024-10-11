import Controller


class User:
    
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.homedir = r"C:\Redes_2\DiretorioAcesso"
        self.permission = "elradfmw"
    
    def addUser(self):
        Controller.createUser(self.username, self.password, self.homedir)
                
    def adicionarAutorizer(user):
        Controller.addAutorizer(user.username, user.password, user.homedir)
        
        
    def print_user(self):
        print(f"Name: {self.name}, Age: {self.age}")