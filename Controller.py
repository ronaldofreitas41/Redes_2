from Db import db, User
import User as u
#Conectando servidor com o banco de dados de usuarios
db.connect()

#Criando tabela no banco de dados
db.create_tables([User])


#Criando Objeto Usuário 
def createUser(username, password, homeDir):
    user = u(username=username, password=password, homeDir=homeDir)
    user.addUser()

def 

def getUser(username):
    user = User.select().where(User.username == username).get()
    usuario  = u(username=user.username, password=user.password, homeDir=user.homeDir)
    return usuario


def createUserDB(username, password, homeDir):
    user = User(username=username, password=password, homeDir=homeDir)
    user.save()