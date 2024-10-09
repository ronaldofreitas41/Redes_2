from pyftpdlib.authorizers import DummyAuthorizer 
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer
# import Controller as c
# import User

# u:User 

# def operations(op):
#     match(op):
    
#         case 1:
#             username = input("Digite o nome do usuário: ")
#             password = input("Digite a senha do usuário: ")
#             c.addUser(username, password)
        
#         case 2:
#             id = input("Digite o id do usuário: ")
#             u = c.deleteUser(id)
          
#         case 3:
#             username = input("Digite o nome do usuário: ")
#             u = c.getUser(username)
#         case 4:
#             id = input("Digite o id do usuário: ")
#             u = c.getUserByID(id)
    
    


#definindo parametros do servidor
authorizer = DummyAuthorizer()  # Gerencia os usuarios que irão acessar o File Server
handler = FTPHandler
authorizer.add_user("ronaldo", "12345", r"D:\facul\Redes_2\DiretorioAcesso", perm="elradfmw") #Adicionando usuario ao File Server
handler.authorizer = authorizer


ipMaquina = "192.168.2.113" #IP da maquina que vai rodar o servidor
port = 21 #Porta que o servidor vai rodar

with FTPServer((ipMaquina,port), handler) as server:
    server.max_cons = 10 #Numero maximo de conexoes
    server.max_cons_per_ip = 5 #Numero maximo de conexoes por IP
    server.serve_forever() #Inicia o servidor


