from socket import *

serverName = 'localhost'
serverPort = 12000
path = '/received'
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName,serverPort))
while 1:
    message = raw_input('Input lowercase sentence:')
    if message == 'q':
        break
    clientSocket.send(message)
    tokens = message.spit(" ")
    if tokens[0] == 'iWant':
        file = tokens[1]
        new_path = raw_input('Directory:')
        if new_path != '':
            path = new_path
        path = path + file
        f = open(path, 'w')
        fileMessage = clientSocket.recv(1024)
        while fileMessage:
            f.write(fileMessage)
            fileMessage = clientSocket.recv(1024)
        f.close()
        continue
    modifiedMessage = clientSocket.recv(1024)
    print 'From Server:', modifiedMessage
clientSocket.close()
