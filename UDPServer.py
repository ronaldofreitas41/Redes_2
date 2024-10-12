import socket
import os

# Configurações do servidor
HOST = '127.0.0.1'  # Endereço IP do servidor
PORT = 65432        # Porta do servidor

def handle_client(client_socket):
    try:
        # Recebe o nome do arquivo do cliente
        filename = client_socket.recv(1024).decode()
        file_path = os.path.join(r"C:\Redes_2\DiretorioAcesso", filename)

        if os.path.exists(file_path):
            with open(file_path, 'rb') as file:
                while True:
                    data = file.read(1024)
                    if not data:
                        break
                    client_socket.sendall(data)
            print(f"Arquivo {filename} enviado com sucesso.")
        else:
            client_socket.sendall(b"ERRO: Arquivo nao encontrado.")
            print(f"Arquivo {filename} não encontrado.")
    except Exception as e:
        print(f"Erro ao lidar com o cliente: {e}")
    finally:
        client_socket.close()

def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((HOST, PORT))
        server_socket.listen()
        print(f"Servidor TCP rodando em {HOST}:{PORT}")

        while True:
            client_socket, addr = server_socket.accept()
            print(f"Conexão estabelecida com {addr}")
            handle_client(client_socket)

if __name__ == "__main__":
    start_server()