import socket as sock
import threading

# Lists to track users and connections
lista_nome = []
lista_conexoes = []

def broadcast(mensagem, remetente_sock_conn=None):
    # Send the message to all connected clients except the sender
    for sock_conn in lista_conexoes:
        if sock_conn != remetente_sock_conn:
            try:
                sock_conn.sendall(mensagem.encode("utf-8"))
            except:
                print("Erro ao enviar mensagem para um cliente:")

def privado(sock_conn, mensagem):
    # Attempt to send a private message
    try:
        _, usuario_escolhido, conteudo_mensagem = mensagem.split(" ", 2)
        for i, nome in enumerate(lista_nome):
            if nome == usuario_escolhido:
                lista_conexoes[i].sendall(f"Private message: {conteudo_mensagem}".encode())
                break
        else:
            sock_conn.sendall(f"User {usuario_escolhido} not found.".encode())
    except ValueError:
        sock_conn.sendall("Invalid format. Use 'privado <username> <message>'.".encode())

def recebe_nome(sock_conn):
    # Receive and return the user's name
    nome = sock_conn.recv(50).decode().strip()
    lista_nome.append(nome)
    lista_conexoes.append(sock_conn)
    broadcast(f"{nome} has joined the chat!", sock_conn)
    return nome

def lista_usuarios(sock_conn):
    # List all connected users
    if lista_nome:
        sock_conn.sendall(f"Usuários conectados: {', '.join(lista_nome)}".encode("utf-8"))
    else:
        sock_conn.sendall("Nenhum usuário conectado.".encode("utf-8"))

def recebe_mensagem(sock_conn):
    nome = recebe_nome(sock_conn)
    while True:
        mensagem = sock_conn.recv(1024).decode()

        if not mensagem:
            lista_nome.remove(nome)
            lista_conexoes.remove(sock_conn)
            sock_conn.close()
            break

        if mensagem.lower() == "usuario":
            lista_usuarios(sock_conn)
        elif mensagem.lower() == "exit":
            lista_nome.remove(nome)
            lista_conexoes.remove(sock_conn)
            sock_conn.close()
            break
        elif mensagem.startswith("privado"):
            privado(sock_conn, mensagem)
        else:
            broadcast(f"{nome} >> {mensagem}", sock_conn)

HOST = '127.0.0.1'
PORTA = 9999

# Create and start the server
sock_server = sock.socket(sock.AF_INET, sock.SOCK_STREAM)
sock_server.bind((HOST, PORTA))
sock_server.listen()
print(f"O servidor {HOST}:{PORTA} está aguardando conexões...")

while True:
    conn, _ = sock_server.accept()
    threadCliente = threading.Thread(target=recebe_mensagem, args=(conn,))
    threadCliente.start()
