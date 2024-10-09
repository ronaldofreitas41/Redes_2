from Db import db, User
import User as u
#Conectando servidor com o banco de dados de usuarios
db.connect()

#Criando tabela no banco de dados
db.create_tables([User])


#Criando Objeto Usuário 
def createUser(username, password):
    user = u(username, password)
    user.addUser()

#Criando Usuário no banco de dados
def createUserDB(username, password, ):
    user = User(username=username, password=password)
    user.save()

#Buscando Usuário no banco de dados por ID
def getUserByID(id):
    user = User.select().where(User.id == id).get()
    usuario  = u(username=user.username, password=user.password, homedir = user.homedir)
    return usuario 

#Buscando Usuário no banco de dados por Nome de usuário
def getUser(username):
    user = User.select().where(User.username == username).get()
    usuario  = u(username=user.username, password=user.password, homedir = user.homedir)
    return usuario

#Delete Usuário no banco de dados por ID
def deleteUser(id):
    user = User.select().where(User.id == id).get()
    user.delete_instance()