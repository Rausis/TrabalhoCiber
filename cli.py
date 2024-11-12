import socket as sock
import threading

# Função para lidar com o recebimento de mensagens do servidor
def receber_mensagens(socket_cliente):
    while True:
        try:
            mensagem = socket_cliente.recv(1024).decode()
            if not mensagem:
                break
            print(mensagem)
        except:
            print("Erro ao receber mensagem do servidor.")
            break

# Função para lidar com o envio de mensagens do usuário para o servidor
def enviar_mensagens(socket_cliente):
    while True:
        mensagem = input()  # Recebe a mensagem do usuário
        socket_cliente.sendall(mensagem.encode())  # Envia a mensagem para o servidor

# IP do servidor ao qual queremos nos conectar
HOST = '26.37.64.17'
PORTA = 9999

# Cria a conexão do socket
socket_cliente = sock.socket(sock.AF_INET, sock.SOCK_STREAM)
socket_cliente.connect((HOST, PORTA))

# Recebe o pedido de nome do servidor
nome = socket_cliente.recv(1024).decode()  # Servidor solicita o nome
print(nome)  # Exibe a solicitação do servidor
nome = input()  # Cliente insere seu nome
socket_cliente.sendall(nome.encode())  # Envia o nome para o servidor

# Cria threads para receber e enviar mensagens
thread_receber = threading.Thread(target=receber_mensagens, args=(socket_cliente,))
thread_enviar = threading.Thread(target=enviar_mensagens, args=(socket_cliente,))

# Inicia as threads
thread_receber.start()
thread_enviar.start()

