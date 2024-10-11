from pyftpdlib.authorizers import DummyAuthorizer 
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer


#definindo parametros do servidor
authorizer = DummyAuthorizer()  # Gerencia os usuarios que irão acessar o File Server
handler = FTPHandler
authorizer.add_user("ronaldo", "12345", r"D:\Facul\Redes_2\DiretorioAcesso", perm="elradfmw") #Adicionando usuario padrão ao File Server
handler.authorizer = authorizer


ipMaquina = "26.4.116.9" #IP da maquina que vai rodar o servidor
port = 21 #Porta que o servidor vai rodar

try:
    with FTPServer((ipMaquina, port), handler) as server:
        server.max_cons = 10
        server.max_cons_per_ip = 5
        print(f"Servidor FTP rodando em {ipMaquina}:{port}")
        server.serve_forever()
except Exception as e:
    print(f"Erro ao iniciar o servidor FTP: {e}")

