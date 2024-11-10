import socket as sock
import threading

def menu():
    print("\n" + "="*30)
    print("      MENU DE OPERAÇÕES")
    print("="*30)
    print("Escolha uma das opções abaixo:")
    print("  - Usuario: Mostrar clientes")
    print("  - Sair: Sair do chat")
    print("  - Menu: Exibir o menu")
    print("="*30 + "\n")

# IP do servidor que queremos nos conectar
HOST = '127.0.0.1'
PORTA = 9999

socket_cliente = sock.socket(sock.AF_INET, sock.SOCK_STREAM)

# Cliente solicita conexão
socket_cliente.connect((HOST, PORTA))
print(5 * "*" + " Chat Iniciado " + 5 * "*")
nome = input("Informe seu nome para entrar no chat: ")
socket_cliente.sendall(nome.encode())  # Envia o nome sem nova linha

# Mostra o menu para o cliente
menu()

# Função para receber mensagens do servidor
def receber_mensagens():
    while True:
        try:
            mensagem = socket_cliente.recv(1024).decode()  # Recebe mensagens do servidor
            print(mensagem)  # Mostra a mensagem recebida
        except:
            print("Erro ao receber mensagem:")
            break

#thread para receber mensagens
thread_receber = threading.Thread(target=receber_mensagens)
thread_receber.start()

while True:
    mensagem = input('Digite sua mensagem ou escolha uma opção: ')

    if mensagem.lower() == "menu":
        menu()
    
    elif mensagem.lower() == "usuario":
        socket_cliente.sendall("usuario".encode())  # Request user list
        usuarios_recebidos = socket_cliente.recv(1024).decode()
        print(f"Users connected: {usuarios_recebidos}")

    elif mensagem.lower().startswith("privado"):
        usuario_escolhido = input("Enter the username for private message: ")
        msg_content = input("Enter your private message: ")
        mensagem_privada = f"privado {usuario_escolhido} {msg_content}"
        socket_cliente.sendall(mensagem_privada.encode("utf-8"))

    elif mensagem.lower() == "sair":
        print("Exiting chat...")
        socket_cliente.sendall("exit".encode())
        socket_cliente.close()
        break

    else:
        # Send regular message to the server
        socket_cliente.sendall(mensagem.encode("utf-8"))
