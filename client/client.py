import socket
import threading
import tkinter as tk
from tkinter import simpledialog, scrolledtext
from cryptography.fernet import Fernet

HOST = '127.0.0.1'
PORT = 5555
# Mesma chave do servidor
CHAVE_SECRETA = b'8coS7jL-u5Qy2cZ-WwFzN6gXo3Rj9kP1lM4nB8vT2qA='
cipher = Fernet(CHAVE_SECRETA)

class ClienteChat:
    def __init__(self):
        msg = tk.Tk()
        msg.withdraw() # Esconde janela principal
        
        self.nickname = simpledialog.askstring("Nome", "Escolha seu apelido:", parent=msg)
        if not self.nickname: return

        self.gui_concluido = False
        self.running = True

        # Configuração da Janela
        self.win = tk.Tk()
        self.win.title(f"Chat - {self.nickname}")
        self.win.configure(bg="lightgray")

        self.texto_area = scrolledtext.ScrolledText(self.win)
        self.texto_area.pack(padx=20, pady=5)
        self.texto_area.config(state='disabled')

        self.msg_label = tk.Label(self.win, text="Mensagem:", bg="lightgray")
        self.msg_label.pack(padx=20, pady=5)

        self.input_area = tk.Entry(self.win)
        self.input_area.pack(padx=20, pady=5, fill=tk.X)
        self.input_area.bind("<Return>", self.write) # Enter envia msg

        self.gui_concluido = True

        # Conexão Socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((HOST, PORT))

        # Thread para receber mensagens
        gui_thread = threading.Thread(target=self.receive)
        gui_thread.daemon = True
        gui_thread.start()

        self.win.protocol("WM_DELETE_WINDOW", self.stop)
        self.win.mainloop()

    def write(self, event=None):
        message = f"{self.nickname}: {self.input_area.get()}"
        
        # 1. Criptografa ANTES de enviar
        #token = cipher.encrypt(message.encode('utf-8'))
        token = message.encode('utf-8')
        
        self.sock.send(token)
        
        # Mostra minha própria mensagem na tela (descriptografada, claro)
        self.texto_area.config(state='normal')
        self.texto_area.insert('end', message + '\n')
        self.texto_area.yview('end')
        self.texto_area.config(state='disabled')
        self.input_area.delete(0, 'end')

    def receive(self):
        while self.running:
            try:
                # Recebe mensagem criptografada
                message_encrypted = self.sock.recv(1024)
                if not message_encrypted: break
                
                # 2. Descriptografa para ler
                message_decrypted = message_encrypted.decode('utf-8')
                
                if self.gui_concluido:
                    self.texto_area.config(state='normal')
                    self.texto_area.insert('end', message_decrypted + '\n')
                    self.texto_area.yview('end')
                    self.texto_area.config(state='disabled')
            except ConnectionAbortedError:
                break
            except Exception as e:
                print(f"Erro: {e}")
                self.sock.close()
                break

    def stop(self):
        self.running = False
        self.win.destroy()
        self.sock.close()
        exit(0)

ClienteChat()