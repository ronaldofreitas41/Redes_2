import tkinter as tk
from tkinter import messagebox, simpledialog, filedialog
from ftplib import FTP, error_perm
import socket

# Função para transferir arquivo via UDP
def download_file_via_udp(server_address, file_name, save_path):
    udp_client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # Envia solicitação ao servidor para receber o arquivo
        udp_client.sendto(file_name.encode(), server_address)

        with open(save_path, 'wb') as f:
            while True:
                data, addr = udp_client.recvfrom(1024)
                if not data:
                    break
                f.write(data)

        messagebox.showinfo("Sucesso", f"Arquivo {file_name} baixado com sucesso via UDP.")
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao baixar o arquivo via UDP: {e}")
    finally:
        udp_client.close()

class FTPClientApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Cliente FTP com Download via UDP")
        self.ftp = None
        self.server_address = None
        
        # Botões para operações
        self.btn_connect = tk.Button(root, text="Conectar ao Servidor FTP", command=self.connect_to_ftp)
        self.btn_connect.grid(row=0, column=0, padx=5, pady=5)
        
        self.btn_list_files = tk.Button(root, text="Listar Arquivos no Servidor", command=self.list_files, state=tk.DISABLED)
        self.btn_list_files.grid(row=1, column=0, padx=5, pady=5)
        
        self.btn_download_file = tk.Button(root, text="Baixar Arquivo via UDP", command=self.download_file, state=tk.DISABLED)
        self.btn_download_file.grid(row=2, column=0, padx=5, pady=5)
    
    def connect_to_ftp(self):
        """
        Conecta ao servidor FTP.
        """
        server_ip = simpledialog.askstring("Conectar ao FTP", "Digite o IP do servidor FTP:")
        server_port = simpledialog.askinteger("Conectar ao FTP", "Digite a porta do servidor FTP:", initialvalue=21)
        username = simpledialog.askstring("Conectar ao FTP", "Digite o nome do usuário:")
        password = simpledialog.askstring("Conectar ao FTP", "Digite a senha:", show='*')
        
        try:
            self.ftp = FTP()
            self.ftp.connect(server_ip, server_port)
            self.ftp.login(username, password)
            self.server_address = (server_ip, server_port)
            messagebox.showinfo("Sucesso", f"Conectado ao servidor FTP {server_ip}:{server_port}")
            self.btn_list_files.config(state=tk.NORMAL)
            self.btn_download_file.config(state=tk.NORMAL)
        except error_perm as e:
            messagebox.showerror("Erro", f"Erro na autenticação: {e}")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao conectar ao servidor FTP: {e}")
    
    def list_files(self):
        """
        Lista os arquivos disponíveis no servidor FTP.
        """
        try:
            files = self.ftp.nlst()
            files_list = "\n".join(files)
            messagebox.showinfo("Arquivos no Servidor", f"Arquivos disponíveis:\n{files_list}")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao listar os arquivos: {e}")
    
    def download_file(self):
        """
        Baixa um arquivo selecionado via UDP.
        """
        file_name = simpledialog.askstring("Baixar Arquivo", "Digite o nome do arquivo para baixar:")
        save_path = filedialog.asksaveasfilename(title="Salvar Arquivo", defaultextension=".txt")
        
        if file_name and save_path:
            try:
                download_file_via_udp(self.server_address, file_name, save_path)
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao baixar o arquivo: {e}")
        else:
            messagebox.showwarning("Atenção", "Nome do arquivo ou caminho de salvamento não podem estar vazios.")

# Inicializar a interface gráfica
if __name__ == "__main__":
    root = tk.Tk()
    app = FTPClientApp(root)
    root.mainloop()
