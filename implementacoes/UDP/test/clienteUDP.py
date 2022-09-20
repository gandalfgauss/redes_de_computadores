import socket
import time
import sys
from random import randint

def lerArquivo():
    """Funcao que leh os dados de arquivo de entrada e retorna cada linha lida"""

    #se o nome do arquivo nao for passado ao executar o programa, tentarah abrir o arquivo "modelo_entrada.txt"
    if len(sys.argv) > 1:
        nomeDoArquivo = sys.argv[1]
    else:
        nomeDoArquivo = "modelo_entrada.txt"

    #ler dados relevantes do arquivo
    dadosDoArquivo = []
    with open(nomeDoArquivo) as arquivo:
        #para cada linha do arquivo
        for linha in arquivo:
            #remover linhas vazias
            if linha != "\n":
                #remover comentarios e adicionar como dados validos
                if len(linha) >1:
                    if linha[0] != "/" and linha[1] != "/":
                        dadosDoArquivo.append(linha.replace("\n", ""))
                else:
                    dadosDoArquivo.append(linha.replace("\n", ""))

    return dadosDoArquivo

#ler dados do arquivo
dadosDoArquivo = lerArquivo()

#atribuir quantidade de dados
quantidadeDeDados = int(dadosDoArquivo[0])

#atribuir dados
dados = dadosDoArquivo[1::]

#definir o host ("IP") e a porta
host = 'localhost'
porta = 8080

#tamanho do buffer para receber dados
buffer = 1024

#criar um socket
cliente = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

print("\nEnviando dados ao Servidor...")

respostas = []
try:
    #para cada dado a ser enviado para o servidor
    for dado in dados:
        #envia o dado
        time.sleep(randint(0,3))
        cliente.sendto(dado.encode(), (host, porta))

        #recebe o processamento do dado
        cliente.settimeout(60.0)
        resposta, endereco = cliente.recvfrom(buffer)
        # reseta o timeout
        cliente.settimeout(None)

        #imprime o resultado dado pelo servidor
        print(resposta.decode())

        #adiciona na lista de respostas
        respostas.append(resposta.decode())
except ConnectionResetError:
    print("Deu o time out e nao chegou mais dados")
except socket.timeout:
    print("Deu o time out e nao chegou mais dados")

#fecha o socket
cliente.close()

#escrever os resultados no arquivo "modelo_saida.txt"
with open("modelo_saida.txt", 'w') as arquivo:
    for resposta in respostas:
        arquivo.write(resposta + "\n")







