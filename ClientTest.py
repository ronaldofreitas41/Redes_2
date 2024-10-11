from tkinter import filedialog
from ftplib import FTP

ftp = FTP('192.168.2.195')
ftp.login('ronaldo', '12345')

# Listar arquivos no diretório atual
files = ftp.nlst()
print("Arquivos disponíveis:", files)


save_path = filedialog.asksaveasfilename(defaultextension=".txt", title="Salvar Arquivo")
print("Caminho de salvamento:", save_path)

if save_path:
    with open(save_path, 'wb') as f:
        ftp.retrbinary('RETR Teste.txt', f.write)

# Desconectar
ftp.quit()
