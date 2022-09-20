import socket
from collections import Counter
import time
from random import randint
import threading


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


def lidarComCliente(dado, enderecoDoCliente):
    """essa funcao vai lidar com todos uma requisicao de um cliente """

    #executar servico

    # contar caracteres do dado recebido
    contagem = contarCaracteres(dado.decode())

    # enviar resultado para cliente
    time.sleep(randint(0, 3))
    servidor.sendto(contagem.encode(), enderecoDoCliente)

    print("Cliente ", enderecoDoCliente, " atendido !")



buffer = 1024

ip = 'localhost'
porta = 8080

#AF_INET -> servico IPv4, SOCK_DGRAM -> Protocolo UDP
servidor = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

#cria o servidor com o endereco de ip e porta esepecificados acima
servidor.bind((ip, porta))


print("Servidor Iniciado", ip, porta)


#vai lidar com clientes enquanto nao houver inatividade, ou seja, timeout
while True:
    try:
        # receber dado de algum cliente qualquer
        # se nao receber nenhum dado em 60 segundos o programa eh encerrado por inatividade
        servidor.settimeout(60.0)
        dado, enderecoDoCliente = servidor.recvfrom(buffer)
        print("Dado de Cliente ", enderecoDoCliente, "recebido !")
        # resetar o timeout
        servidor.settimeout(None)

    except ConnectionResetError:
        print("Deu o time out")
        NaoDeuTimeOut = False
        break
    except socket.timeout:
        print("Deu o time out")
        NaoDeuTimeOut = False
        break

    #cria uma thread de execucao para contar os caracterers e enviar para o cliente que solicitou o servico
    #enquanto isso novas conexoes sao aceitas
    thread = threading.Thread(target=lidarComCliente, args=(dado, enderecoDoCliente,))
    thread.start()

servidor.close()











