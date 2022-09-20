import socket
import threading
import math
from collections import Counter
import time


def eh_numero(caractere):
    """funcao que recebe um caractere e retorna true se ele eh um numero e false caso contrario"""
    if 48 <= ord(caractere) <= 57:
        return True

    return False


def eh_vogal(caractere):
    """funcao que recebe um caractere e retorna true se ele eh uma vogal e false caso contrario"""
    if caractere in "aeiouAEIOU":
        return True

    return False

def eh_consoante(caractere):
    """funcao que recebe um caractere e retorna true se ele eh uma consoante e false caso contrario"""
    if caractere in "bcdfghjklmnpqrstvwxyzBCDFGHJKLMNPQRSTVWXYZ":
        return True

    return False


def contarCaracteres(dado):
    """conta os caracteres alfa numericos e retorna uma string com a contagem de consoantes, vogais e numeros"""
    contagem = dict(Counter(dado))

    consoante = 0
    vogais = 0
    numeros = 0

    #confere se os caracteres sao vogais, consoantes, ou numeros e aumenta a contagem de cada tipo de caractere
    for caractere in contagem.keys():
        if eh_consoante(caractere):
            consoante += contagem[caractere]
        elif eh_vogal(caractere):
            vogais += contagem[caractere]
        elif eh_numero(caractere):
            numeros += contagem[caractere]

    #se nao teve nenhuma vogal, consoante ou numeros retorna erro
    if consoante == vogais == numeros == 0:
        return "erro"

    return f'C={consoante};V={vogais};N={numeros}'



def lidarComCliente(socketCliente):
    """funcao que relizarah a execucao de contagem de caracteres de cada solicitacao de cada cliente"""

    endereco = addr

    #recebe mensagem de entrada do cliente
    solicitacao = socketCliente.recv(buffer).decode()
    print("Recebido: ", solicitacao)
    print("\n--------------------------\n")

    #envia mensagem ACK para cliente
    socketCliente.sendall(f'\nMensagem destinada ao cliente {endereco[0]} {endereco[1]} \nACK ! Recebido pelo servidor !\n'.encode())

    #executar servico
    #ler a quantidade de dados que serao enviados
    quantidadeDeDados = int(socketCliente.recv(buffer).decode())

    #receber cada um dos dados
    dados = []
    for i in range(quantidadeDeDados):
        dado = ""
        #receber tamanho do dado
        tamanhoDoDado = int(socketCliente.recv(buffer).decode())

        #repete do loop 'n' vezes, quem 'n' eh o numero de vezes que o dado completo cabe no buffer
        for j in range(math.ceil(tamanhoDoDado/buffer)):
            dado = dado + socketCliente.recv(buffer).decode()

        dados.append(dado)

    #contar caracteres de todos os dados enviados pelo cliente
    contagem = list(map(contarCaracteres, dados))

    #enviar resultados para cliente
    for cont in contagem:
        socketCliente.sendall(cont.encode())
        time.sleep(0.5)

    #solicitar o termino da execucao
    socketCliente.sendall("Termine a execucao !".encode())

    print("Cliente ", endereco, "atendido !")
    #fechar conexao
    socketCliente.close()

ip = 'localhost'
porta = 8080

buffer = 50

#AF_INET -> servico IPv4, SOCK STREAM -> Protocolo Tcp
servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#cria o servidor com o endereco de ip e porta esepecificados acima
servidor.bind((ip, porta))

MAXIMOCONEXOES =2

#determinar o numero maximo de conexoes simultaneas
servidor.listen(MAXIMOCONEXOES)

print("Escutando", ip, porta)

NaoDeuTimeOut = True

#enquanto nao der um timeout ou seja, enquanto chegar conexoes repete o laco abaixo
while NaoDeuTimeOut:
    try:
        #timeout de 60 segundos para que chegue uma conexao
        servidor.settimeout(60)
        cliente, addr = servidor.accept() #retorna o cliente e as informacoes da conexao
        servidor.settimeout(None)

    except ConnectionResetError:
        print("Deu o time out, nenhuma nova conexao")
        NaoDeuTimeOut = False
        # espera 30 segundos antes de terminar a execucao do servidor
        # para dar tempo de alguns cliente terminarem de executar
        # neste momento o sevidor nao aceita mais conexoes
        time.sleep(30)
        break
    except socket.timeout:
        print("Deu o time out, nenhuma nova conexao")
        NaoDeuTimeOut = False
        # espera 30 segundos antes de terminar a execucao do servidor
        # para dar tempo de alguns cliente terminarem de executar
        # neste momento o sevidor nao aceita mais conexoes
        time.sleep(30)
        break

    print("Conexao aceita de:", addr[0], addr[1])

    #cria uma thread para cada cliente aceito
    socketCliente = threading.Thread(target=lidarComCliente, args=(cliente,))

    socketCliente.start()














