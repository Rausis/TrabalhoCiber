import socket as sock
import threading

# Function to handle receiving messages from the server
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

# Function to handle sending user input to the server
def enviar_mensagens(socket_cliente):
    while True:
        mensagem = input()  # Get user input
        socket_cliente.sendall(mensagem.encode())  # Send the message to the server

# IP do servidor que queremos nos conectar
HOST = '127.0.0.1'
PORTA = 9999

# Create socket connection
socket_cliente = sock.socket(sock.AF_INET, sock.SOCK_STREAM)
socket_cliente.connect((HOST, PORTA))

# Recebe o pedido de nome do servidor
nome = socket_cliente.recv(1024).decode()  # Server asks for the name
print(nome)  # Display the prompt from the server
nome = input()  # Client enters their name
socket_cliente.sendall(nome.encode())  # Send name to server

# Create threads for receiving and sending messages
thread_receber = threading.Thread(target=receber_mensagens, args=(socket_cliente,))
thread_enviar = threading.Thread(target=enviar_mensagens, args=(socket_cliente,))

# Start the threads
thread_receber.start()
thread_enviar.start()

# Join threads to wait for completion
thread_receber.join()
thread_enviar.join()
