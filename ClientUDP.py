import tkinter as tk
from tkinter import messagebox, simpledialog, filedialog
import socket
import struct
import hashlib

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
        server_ip = simpledialog.askstring("Conectar ao UDP", "Digite o IP do servidor UDP:")
        server_port = simpledialog.askinteger("Conectar ao UDP", "Digite a porta do servidor UDP:", initialvalue=2000)
        
        self.server_address = (server_ip, server_port)
        messagebox.showinfo("Conexão", f"Conectado ao servidor UDP {server_ip}:{server_port}")
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
            if self.authenticate_user():  # Tenta autenticar antes de baixar
                self.request_file(filename)
            else:
                messagebox.showwarning("Atenção", "Autenticação falhou. Não é possível solicitar o arquivo.")
        else:
            messagebox.showwarning("Atenção", "Nome do arquivo não pode estar vazio.")

    def request_file(self, filename):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto(f"FILE_REQUEST|{filename}".encode('utf-8'), self.server_address)

        # Solicita ao usuário o caminho onde salvar o arquivo
        save_path = filedialog.asksaveasfilename(defaultextension=".txt", title="Salvar Arquivo", initialfile=filename)

        if not save_path:
            messagebox.showwarning("Atenção", "Caminho de salvamento não definido.")
            return
        
        with open(save_path, "wb") as f:
            packet_number = 0

            while True:
                try:
                    sock.settimeout(2)
                    packet, _ = sock.recvfrom(1500)  # Receber pacote completo
                    
                    # Verifique se o pacote recebido tem o tamanho correto
                    if len(packet) < 36:
                        # Verifica se o pacote é uma mensagem de erro
                        if packet.decode('utf-8').startswith("ERRO"):
                            print(packet.decode('utf-8'))
                            break
                        print("Pacote recebido é menor que 36 bytes. Ignorando.")
                        continue

                    # Extrair número do pacote e dados
                    header = struct.unpack("i32s", packet[:36])
                    received_packet_number, received_checksum = header
                    data = packet[36:]

                    # Verifica se é o último pacote
                    if data == b"END":
                        print("Recebido fim da transmissão.")
                        break

                    # Verifica o número do pacote
                    if received_packet_number == packet_number:
                        # Verifica checksum
                        if self.calculate_checksum(data).encode('utf-8') == received_checksum:
                            f.write(data)
                            print(f"Pacote {received_packet_number} recebido corretamente.")
                            # Envia ACK
                            sock.sendto(struct.pack("i", packet_number), self.server_address)
                            packet_number += 1
                        else:
                            print(f"Checksum falhou para o pacote {received_packet_number}. Retransmitindo.")
                    else:
                        print(f"Número do pacote inesperado {received_packet_number}. Ignorando.")
                except socket.timeout:
                    print("Timeout! Nenhum pacote recebido.")

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
