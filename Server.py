from pyftpdlib.authorizers import DummyAuthorizer 
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer




#definindo parametros do servidor
authotizer = DummyAuthorizer() # Gerencia os usuarios que irão acessar o File Server
handler = FTPHandler
handler.authorizer = authorizer

ipMaquina = "200.239.155.122" #IP da maquina que vai rodar o servidor
port = 21 #Porta que o servidor vai rodar

with FTPServer((ipMaquina,port), handler) as server:
    server.max_cons = 10 #Numero maximo de conexoes
    server.max_cons_per_ip = 5 #Numero maximo de conexoes por IP
    server.serve_forever() #Inicia o servidor


