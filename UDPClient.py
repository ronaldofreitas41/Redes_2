import tkinter as tk
from tkinter import messagebox, simpledialog, filedialog
import socket
import struct
import hashlib

SERVER_IP = "127.0.0.1"  
SERVER_PORT = 65432   

class UDPClientApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gerenciador de Usuários e Cliente UDP")
        self.server_address = None
        
        # Sessão de gerenciamento de usuários
        self.lbl_user_section = tk.Label(root, text="Gerenciamento de Usuários", font=("Arial", 12, "bold"))
        self.lbl_user_section.grid(row=0, column=0, columnspan=2, pady=10)

        self.btn_add_user = tk.Button(root, text="Adicionar Usuário", command=self.add_user)
        self.btn_add_user.grid(row=1, column=0, padx=5, pady=5)

        self.btn_delete_user = tk.Button(root, text="Excluir Usuário", command=self.delete_user)
        self.btn_delete_user.grid(row=2, column=0, padx=5, pady=5)

        self.btn_get_user = tk.Button(root, text="Buscar Usuário", command=self.get_user)
        self.btn_get_user.grid(row=3, column=0, padx=5, pady=5)

        self.btn_get_user_by_id = tk.Button(root, text="Buscar Usuário por ID", command=self.get_user_by_id)
        self.btn_get_user_by_id.grid(row=4, column=0, padx=5, pady=5)

        # Sessão de operações UDP
        self.lbl_udp_section = tk.Label(root, text="Operações UDP", font=("Arial", 12, "bold"))
        self.lbl_udp_section.grid(row=5, column=0, columnspan=2, pady=10)

        self.btn_connect = tk.Button(root, text="Conectar ao Servidor UDP", command=self.connect_to_udp)
        self.btn_connect.grid(row=6, column=0, padx=5, pady=5)

        self.btn_list_files = tk.Button(root, text="Listar Arquivos Disponíveis", command=self.list_files, state=tk.DISABLED)
        self.btn_list_files.grid(row=7, column=0, padx=5, pady=5)

        self.btn_download_file = tk.Button(root, text="Baixar Arquivo via UDP", command=self.download_file, state=tk.DISABLED)
        self.btn_download_file.grid(row=8, column=0, padx=5, pady=5)

    def connect_to_udp(self):
        SERVER_IP = simpledialog.askstring("Conectar ao UDP", "Digite o IP do servidor UDP:",initialvalue= "192.168.")
        SERVER_PORT = simpledialog.askinteger("Conectar ao UDP", "Digite a porta do servidor UDP:", initialvalue=2000)
        
        self.server_address = (SERVER_IP, SERVER_PORT)
        messagebox.showinfo("Conexão", f"Conectado ao servidor UDP {SERVER_IP}:{SERVER_PORT}")
        self.btn_list_files.config(state=tk.NORMAL)
        self.btn_download_file.config(state=tk.NORMAL)

    def authenticate_user(self):
        username = simpledialog.askstring("Usuário", "Digite seu nome de usuário:")
        password = simpledialog.askstring("Senha", "Digite sua senha:", show='*')

        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto(f"AUTH|{username}|{password}".encode('utf-8'), self.server_address)
        print(f"Enviando autenticação: AUTH|{username}|{password}")

        # Espera pela resposta do servidor
        try:
            sock.settimeout(2)
            response, _ = sock.recvfrom(1024)
            print(f"Resposta recebida: {response.decode('utf-8')}")
            if response.decode('utf-8') == "AUTH_OK":
                print("Autenticação bem-sucedida!")
                return True
            else:
                print("Falha na autenticação.")
                return False
        except socket.timeout:
            print("Timeout ao tentar autenticar.")
            return False

    def list_files(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto("LIST_FILES".encode('utf-8'), self.server_address)

        try:
            sock.settimeout(2)
            files_response, _ = sock.recvfrom(1024)
            files = files_response.decode('utf-8').splitlines()
            files_list = "\n".join(files)
            messagebox.showinfo("Arquivos Disponíveis", files_list)
        except socket.timeout:
            messagebox.showerror("Erro", "Timeout ao tentar listar os arquivos.")

    def download_file(self):
        filename = simpledialog.askstring("Nome do Arquivo", "Informe o nome do arquivo a ser baixado:")
        if filename:
            print(f"Baixando arquivo {filename}...")
            print("Server IP: ", SERVER_IP)
            print("Server PORT: ", SERVER_PORT)
            self._download_file(SERVER_IP, SERVER_PORT, filename)

    def _download_file(self, host, port, filename):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            print("Conectando ao servidor...")
            print("Host: ", host)
            print("Port: ", port)
            client_socket.connect((host, port))
            client_socket.sendall(filename.encode())

            with open(f'downloaded_{filename}', 'wb') as file:
                while True:
                    data = client_socket.recv(1024)
                    if not data:
                        break
                    file.write(data)
            print(f"Arquivo {filename} baixado com sucesso.")

    def calculate_checksum(self, data):
        return hashlib.md5(data).hexdigest()

    # Métodos de gerenciamento de usuários (sem alterações)
    def add_user(self):
        username = simpledialog.askstring("Adicionar Usuário", "Digite o nome do usuário:")
        password = simpledialog.askstring("Adicionar Usuário", "Digite a senha do usuário:", show='*')
        
        if username and password:
            try:
                createUserDB(username, password)
                messagebox.showinfo("Sucesso", f"Usuário {username} adicionado com sucesso.")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao adicionar o usuário {username}: {e}")
        else:
            messagebox.showwarning("Atenção", "Nome ou senha não podem estar vazios.")
    
    def delete_user(self):
        user_id = simpledialog.askstring("Excluir Usuário", "Digite o ID do usuário:")
        
        if user_id:
            try:
                deleteUser(user_id)
                messagebox.showinfo("Sucesso", f"Usuário com ID {user_id} excluído com sucesso.")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao excluir o usuário com ID {user_id}: {e}")
        else:
            messagebox.showwarning("Atenção", "O ID do usuário não pode estar vazio.")
    
    def get_user(self):
        username = simpledialog.askstring("Buscar Usuário", "Digite o nome do usuário:")
        
        if username:
            try:
                user = getUser(username)
                messagebox.showinfo("Usuário Encontrado", f"Usuário {user.username} encontrado com sucesso.\nHomedir: {user.homedir}")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao buscar o usuário {username}: {e}")
        else:
            messagebox.showwarning("Atenção", "O nome do usuário não pode estar vazio.")
    
    def get_user_by_id(self):
        user_id = simpledialog.askstring("Buscar Usuário por ID", "Digite o ID do usuário:")
        
        if user_id:
            try:
                user = getUserByID(user_id)
                messagebox.showinfo("Usuário Encontrado", f"Usuário com ID {user_id} encontrado com sucesso.\nNome: {user.username}\nHomedir: {user.homedir}")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao buscar o usuário com ID {user_id}: {e}")
        else:
            messagebox.showwarning("Atenção", "O ID do usuário não pode estar vazio.")

# Inicializar a interface gráfica
if __name__ == "__main__":
    root = tk.Tk()
    app = UDPClientApp(root)
    root.mainloop()
