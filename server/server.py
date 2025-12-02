import socket
import threading
import tkinter as tk

import os
from dotenv import load_dotenv

from tkinter import scrolledtext
from cryptography.fernet import Fernet

# --- CONFIGURAÇÕES ---
load_dotenv()

HOST = os.getenv('HOST')
PORT = int(os.getenv('PORT')) # Converte para int, pois vem como string
KEY_STRING = os.getenv('APP_KEY')

if not KEY_STRING:
    print("ERRO: APP_KEY não encontrada no arquivo .env")
    exit()

CHAVE_SECRETA = KEY_STRING.encode('utf-8') 
cipher = Fernet(CHAVE_SECRETA)

clients = []

def iniciar_servidor():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()
    log_msg(f"Servidor iniciado em {HOST}:{PORT}")
    log_msg("Aguardando conexões...")

    # Thread para aceitar clientes sem travar a GUI
    thread_aceitar = threading.Thread(target=aceitar_conexoes, args=(server,))
    thread_aceitar.daemon = True
    thread_aceitar.start()

def aceitar_conexoes(server):
    while True:
        client_sock, addr = server.accept()
        clients.append(client_sock)
        log_msg(f"Nova conexão: {addr}")
        
        # Thread dedicada para cada cliente
        thread_cliente = threading.Thread(target=tratar_cliente, args=(client_sock, addr))
        thread_cliente.daemon = True
        thread_cliente.start()

def tratar_cliente(conn, addr):
    while True:
        try:
            # Recebe dados brutos (criptografados)
            msg_encrypted = conn.recv(1024)
            if not msg_encrypted:
                break
            
            # Descriptografar para ler no Servidor
            try:
                msg_decrypted = cipher.decrypt(msg_encrypted).decode('utf-8')
                texto_log = f"[{addr[1]}]: {msg_decrypted}"
                log_msg(texto_log) # Mostra na GUI do servidor
                
                # Retransmitir a mensagem (broadcast) para os outros que estivem contectados
                broadcast(msg_encrypted, conn)
                
            except Exception as e:
                log_msg(f"Erro de criptografia de {addr}: {e}")

        except:
            clients.remove(conn)
            conn.close()
            log_msg(f"Cliente {addr} desconectou.")
            break

def broadcast(msg_encrypted, connection):
    for client in clients:
        if client != connection:
            try:
                client.send(msg_encrypted)
            except:
                clients.remove(client)

# --- FUNÇÕES DA INTERFACE ---
def log_msg(msg):
    # Atualiza a caixa de texto da GUI
    texto_area.config(state=tk.NORMAL)
    texto_area.insert(tk.END, msg + "\n")
    texto_area.yview(tk.END) # Auto-scroll
    texto_area.config(state=tk.DISABLED)

# --- INICIALIZAÇÃO DA GUI ---
janela = tk.Tk()
janela.title("Servidor de Chat (Monitoramento)")
janela.geometry("500x400")

label = tk.Label(janela, text="Log do Servidor - Mensagens Descriptografadas", font=("Arial", 12))
label.pack(pady=10)

texto_area = scrolledtext.ScrolledText(janela, state=tk.DISABLED)
texto_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

btn_iniciar = tk.Button(janela, text="Iniciar Servidor", command=iniciar_servidor, bg="green", fg="white")
btn_iniciar.pack(pady=5)

janela.mainloop()