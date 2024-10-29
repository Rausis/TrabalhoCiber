import socket as sock

HOST = '127.0.0.1' #IP DO SERVIDOR
PORTA = 9999 #PORTA DO SERVIDOR
#CRIAR SOCKET IPv4/TCP
s = sock.socket(sock.AF_INET,sock.SOCK_STREAM)
#CLIENTE SOLICITA CONEXAO
s.connect((HOST,PORTA))
#CLIENTE EVVIA UMA MENSAGEM
s.sendall(str.encode('BES - PUCPR'))
info = str(input("Texto: "))
texto = sock.socket
texto.sendall(str.encode(info))
#cliente le uma mensagem
dados = s.recv(1024)
print(f'Servidor >> {dados.decode()}')
