import socket

def download_file(host='127.0.0.1', port=65432, filename='Teste.txt'):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((host, port))
        client_socket.sendall(filename.encode())

        with open(f'downloaded_{filename}', 'wb') as file:
            while True:
                data = client_socket.recv(1024)
                if not data:
                    break
                file.write(data)
        print(f"Arquivo {filename} baixado com sucesso.")

if __name__ == "__main__":
    download_file(filename='Teste.txt')  # Altere para o arquivo desejado