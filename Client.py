import tkinter as tk
from tkinter import messagebox, simpledialog
from Controller import createUserDB, deleteUser, getUser, getUserByID

class FTPClientApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gerenciador de Usuários FTP")
        
        # Botões para operações
        self.btn_add_user = tk.Button(root, text="Adicionar Usuário", command=self.add_user)
        self.btn_add_user.grid(row=0, column=0, padx=5, pady=5)
        
        self.btn_delete_user = tk.Button(root, text="Excluir Usuário", command=self.delete_user)
        self.btn_delete_user.grid(row=1, column=0, padx=5, pady=5)
        
        self.btn_get_user = tk.Button(root, text="Buscar Usuário", command=self.get_user)
        self.btn_get_user.grid(row=2, column=0, padx=5, pady=5)
        
        self.btn_get_user_by_id = tk.Button(root, text="Buscar Usuário por ID", command=self.get_user_by_id)
        self.btn_get_user_by_id.grid(row=3, column=0, padx=5, pady=5)
    
    def add_user(self):
        """
        Adiciona um usuário chamando o método do controlador.
        """
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
        """
        Exclui um usuário chamando o método do controlador.
        """
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
        """
        Busca um usuário pelo nome chamando o método do controlador.
        """
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
        """
        Busca um usuário pelo ID chamando o método do controlador.
        """
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
    app = FTPClientApp(root)
    root.mainloop()
