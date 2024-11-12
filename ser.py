import socket as sock
import threading

# Listas para acompanhar os nomes de usuários e conexões
lista_nome = []
lista_conexoes = []

# Função para enviar mensagens a todos os clientes
def broadcast(mensagem, remetente_sock_conn=None):
    for sock_conn in lista_conexoes:
        if sock_conn != remetente_sock_conn:  # Evita enviar de volta para o remetente
            try:
                sock_conn.sendall(mensagem.encode())
            except:
                print("Erro ao enviar mensagem para o chat.")

# Função para enviar mensagens privadas
def privado(sock_conn, mensagem):
    _, usuario_escolhido, conteudo_mensagem = mensagem.split(" ", 2)
    for i, nome in enumerate(lista_nome):
        if nome == usuario_escolhido:
            lista_conexoes[i].sendall(f"Mensagem privada de {nome}: {conteudo_mensagem}".encode())
            break
    else:
        sock_conn.sendall(f"Usuário {usuario_escolhido} não encontrado.".encode())

# Função para listar usuários conectados
def lista_usuarios(sock_conn):
    if lista_nome:
        sock_conn.sendall(f"Usuários conectados: {', '.join(lista_nome)}".encode())
    else:
        sock_conn.sendall("Nenhum usuário conectado.".encode())

# Função para receber o nome do usuário
def recebe_nome(sock_conn):
    sock_conn.sendall("Digite seu nome:".encode())
    nome = sock_conn.recv(50).decode()
    lista_nome.append(nome)
    lista_conexoes.append(sock_conn)
    broadcast(f"{nome} entrou no chat!", sock_conn)
    return nome

# Função para receber e processar mensagens
def recebe_mensagem(sock_conn):
    nome = recebe_nome(sock_conn)
    while True:
        sock_conn.sendall("Digite uma mensagem ou use 'usuario' para listar usuários, 'sair' para sair, ou 'privado <nome> <mensagem>' para mensagem privada:".encode())
        mensagem = sock_conn.recv(1024).decode()

        if not mensagem:
            break

        if mensagem.lower() == "usuario":
            lista_usuarios(sock_conn)
        elif mensagem.lower() == "sair":
            lista_nome.remove(nome)
            lista_conexoes.remove(sock_conn)
            broadcast(f"{nome} saiu do chat.")  # Notifica os outros usuários sobre a saída
            sock_conn.close()
            break
        elif mensagem.startswith("privado"):
            privado(sock_conn, mensagem)
        else:
            broadcast(f"{nome} >> {mensagem}", sock_conn)

# Configurações do servidor
HOST = '26.37.64.17'
PORTA = 9999

sock_server = sock.socket(sock.AF_INET, sock.SOCK_STREAM)
sock_server.bind((HOST, PORTA))
sock_server.listen()
print(f"O servidor {HOST}:{PORTA} está aguardando conexões...")

# Aceita conexões de clientes
while True:
    conn, _ = sock_server.accept()
    threadCliente = threading.Thread(target=recebe_mensagem, args=(conn,))
    threadCliente.start()