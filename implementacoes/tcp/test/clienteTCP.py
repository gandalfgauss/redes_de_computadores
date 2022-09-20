import socket
import time
import sys

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
                        #remove o caractere '\n' que toda linha possui no final
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
cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#conectar a um servidor
try:
    cliente.connect((host, porta))
except ConnectionRefusedError:
    print("\nO servidor nao estah aceitando conexoes !\nPor favor tente novamente em alguns segundos.")
    exit()

cliente.sendall("Eu sou um cliente, estou me conectando ao servidor".encode())

#receber ACK

resposta = cliente.recv(buffer).decode()
print(resposta)

#envia a quantidade de dados que serao enviados
cliente.sendall(str(quantidadeDeDados).encode())
time.sleep(0.2)

#para cada dado
for dado in dados:
    #envia o tamanho dos dados que serao enviados
    cliente.sendall(str(len(dado)).encode())
    time.sleep(0.2)

    #depois envia os dados
    cliente.sendall(dado.encode())
    time.sleep(0.2)


print("\nEsperando Resposta do Servidor !")

#recebe os dados do servidor imprime na tela
respostas = []
for i in range(quantidadeDeDados):
    resposta = cliente.recv(buffer).decode()
    print(resposta)
    respostas.append(resposta)

#mensagem de terminar a execucao
resposta = cliente.recv(buffer).decode()
print(resposta)

#escrever os resultados no arquivo "modelo_saida.txt"
with open("modelo_saida.txt", 'w') as arquivo:
    for resposta in respostas:
        arquivo.write(resposta + "\n")






