import ftplib
from tkinter import filedialog, messagebox, simpledialog
from ftplib import FTP

ftp = FTP('192.168.2.113')
ftp.login('ronaldo', '12345')

# Listar arquivos no diretório atual
files = ftp.nlst()
print("Arquivos disponíveis:", files)


save_path = filedialog.asksaveasfilename(defaultextension=".txt", title="Salvar Arquivo")
print("Caminho de salvamento:", save_path)

nomeArq = simpledialog.askstring("Nome do Arquivo", "Informe o nome do arquivo a ser baixado:")

nomeArq = simpledialog.askstring("Nome do Arquivo", "Informe o nome do arquivo a ser baixado:")

if save_path:
    if nomeArq:
        with open(save_path, 'wb') as f:
            try:
                ftp.retrbinary('RETR ' + nomeArq, f.write)
            except ftplib.error_perm as e:
                messagebox.showerror("Erro", f"Erro ao baixar o arquivo: {e}")
    else:
        messagebox.showerror("Erro", "Nome do arquivo não pode estar vazio.")
else:
    messagebox.showerror("Erro", "Caminho de salvamento não definido.")
# Desconectar
ftp.quit()
