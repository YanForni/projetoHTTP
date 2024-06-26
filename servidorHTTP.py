#implementação de um servidor base para interpratação de métodos HTTP

import socket

#definindo o endereço IP do host
SERVER_HOST = ""
#definindo o número da porta em que o servidor irá escutar pelas requisições HTTP
SERVER_PORT = 8080

#vamos criar o socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#vamos setar a opção de reutilizar sockets já abertos
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

#atrela o socket ao endereço da máquina e ao número de porta definido
server_socket.bind((SERVER_HOST, SERVER_PORT))

#coloca o socket para escutar por conexões
server_socket.listen(1)

#mensagem inicial do servidor
print("Servidor em execução...")
print("Escutando por conexões na porta %s" % SERVER_PORT)

#cria o while que irá receber as conexões
while True:
    #espera por conexões
    #client_connection: o socket que será criado para trocar dados com o cliente de forma dedicada
    #client_address: tupla (IP do cliente, Porta do cliente)
    client_connection, client_address = server_socket.accept()

    #pega a solicitação do cliente
    request = client_connection.recv(1024).decode()
    #verifica se a request possui algum conteúdo (pois alguns navegadores ficam periodicamente enviando alguma string vazia)
    if request:
        #imprime a solicitação do cliente
        #print(request)
        
        #analisa a solicitação HTTP
        headers = request.split("\n")
        verb = headers[0].split()[0]
        #print(headers)#impressão dos cabeçalhos
        #pega o nome do arquivo sendo solicitado
        filename = headers[0].split()[1]
        
        if verb == "PUT":
            try:
                body = request.split("\n")
                newfile = open("htdocs"+filename, "w")
                newfile.seek(0)
                body_content = ''.join(body[body.index('\r')+1: len(body)])
                content = '<html>'+body_content+'</html>'
                newfile.write(content)
                newfile.close()
                response = "HTTP/1.1 200 OK\n\n" + content
                print("Content put in", filename)
            except Exception as ex:
                response = 'HTTP/1.1 500 INTERNAL SERVER ERROR \n\n<h1>ERROR 500!<br>Internal Server Error! <br>'+ex+'</h1>'
                print("Error 500: Internal Server Error\n")
            finally:
                client_connection.sendall(response.encode())
        elif verb == "GET":
            #verifica qual arquivo está sendo solicitado e envia a resposta para o cliente
            if filename == "/":
                filename = "/index.html"

            #try e except para tratamento de erro quando um arquivo solicitado não existir
            try:
                #abrir o arquivo e enviar para o cliente
                fin = open("htdocs" + filename, encoding='utf-8')
                #leio o conteúdo do arquivo para uma variável
                content = fin.read()
                #fecho o arquivo
                fin.close()
                #envia a resposta
                response = "HTTP/1.1 200 OK\nContent-Type: text/html; charset=utf-8\n\n" + content
                print("Got content from", filename)
            except FileNotFoundError:
                #caso o arquivo solicitado não exista no servidor, gera uma resposta de erro
                fin = open("htdocs/404.html", encoding='utf-8')
                content = fin.read()
                fin.close()
                response = "HTTP/1.1 404 NOT FOUND\nContent-Type: text/html; charset=utf-8\n\n" + content
                print("Error 404: "+filename[1:]+" Not Found\n")
            finally:
                #envia a resposta HTTP
                client_connection.sendall(response.encode())
        else:
            print("Verb "+verb+" not implemented.\n")

        client_connection.close()

server_socket.close()


