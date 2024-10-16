import ftplib
import tkinter as tk
from tkinter import messagebox, simpledialog, filedialog
from ftplib import FTP, error_perm
import socket
import threading

from numpy import ptp
from Controller import createUserDB, deleteUser, getUser, getUserByID

class FTPClientApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gerenciador de Usuários e Cliente FTP com Download via UDP")
        self.ftp = None
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

        # Sessão de operações FTP
        self.lbl_ftp_section = tk.Label(root, text="Operações FTP", font=("Arial", 12, "bold"))
        self.lbl_ftp_section.grid(row=5, column=0, columnspan=2, pady=10)

        self.btn_connect = tk.Button(root, text="Conectar ao Servidor FTP", command=self.connect_to_ftp)
        self.btn_connect.grid(row=6, column=0, padx=5, pady=5)
        
        self.btn_list_files = tk.Button(root, text="Listar Arquivos no Servidor", command=self.list_files, state=tk.DISABLED)
        self.btn_list_files.grid(row=7, column=0, padx=5, pady=5)
        
        # Lista de arquivos do servidor
        self.lbl_files = tk.Label(root, text="Arquivos no Servidor:")
        self.lbl_files.grid(row=8, column=0, padx=5, pady=5)

        self.lst_files = tk.Listbox(root, height=10, width=50)
        self.lst_files.grid(row=9, column=0, padx=5, pady=5)

        # Botão de download
        self.btn_download_file = tk.Button(root, text="Baixar Arquivo via UDP pelo Id de arquivo", command=self.download_selected_file, state=tk.DISABLED)
        self.btn_download_file.grid(row=10, column=0, padx=5, pady=5)

    # Métodos de gerenciamento de usuários
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

    # Métodos de operações FTP
    def connect_to_ftp(self):
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
        try:
            files = self.ftp.nlst()
            self.lst_files.delete(0, tk.END)
            for file in files:
                self.lst_files.insert(tk.END, file)
            messagebox.showinfo("Sucesso", "Lista de arquivos atualizada.")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao listar os arquivos: {e}")

    def download_selected_file(self):
        nomeArq = simpledialog.askstring("Nome do Arquivo", "Informe o nome do arquivo a ser baixado:")
        save_path = filedialog.asksaveasfilename(defaultextension=".txt", title="Salvar Arquivo")
        print("Caminho de salvamento:", save_path)# Substitua pelo caminho correto

        if save_path:
            if nomeArq:
                try:
                    with open(save_path, 'wb') as f:
                        self.ftp.retrbinary('RETR ' + nomeArq, f.write)
                except ftplib.error_perm as e:
                    messagebox.showerror("Erro", f"Erro ao baixar o arquivo: {e}")
            else:
                messagebox.showerror("Erro", "Nome do arquivo não pode estar vazio.")
        else:
            messagebox.showerror("Erro", "Caminho de salvamento não definido.")
        
# Inicializar a interface gráfica
if __name__ == "__main__":
    root = tk.Tk()
    app = FTPClientApp(root)
    root.mainloop()
