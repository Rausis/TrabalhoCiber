import socket as sock

HOST = 'localhost' #127.0.0.1
PORTA = 9999


#IPv4(primeiro parametro): AF_INET
# CRIAR O SOCKED DO SERVIDOR
s = sock.socket(sock.AF_INET,sock.SOCK_STREAM)

#FAZEMOS O "PLUG" DO IP COM A PORTA(BIND)
s.bind((HOST,PORTA))
#COLOCAMOS O SERVIDOR NO MODO DE ESCUTA(LISTEN)-AGUARDANDO CONECXOES
s.listen()
print(f'O Server {HOST}:{PORTA} esta aguardndo conexoes...')


#SERVIDOR PRECISA ACEITA CONEXOES
while True:
    conn, ender = s.accept()
    print(f'Conexao estabilicida com {ender}')
    #RECEBIMENTO DE MENSAGEM
    dados = conn.recv(1024)
    print(f'Cliente: {ender} >> {dados.decode()}')
    #ENVIO DE MENSAGEM (bytes)
    conn.sendall(dados)

