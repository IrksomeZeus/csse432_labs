# Douglas Wise and Austin Yates
# CSSE432 Computer Networks - Lab 2
# March 31, 2017

from socket import *
import os.path

serverName = 'localhost'
serverPort = 12000

def main():
    path = './received/'
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((serverName,serverPort))
    print 'Client started.\nValid commands are iWant <filename> and uTake <filename>\nEnter \'q\' to quit.'
    while 1:
        message = raw_input('Client>')
        if message == 'q':
            break
        clientSocket.send(message)
        tokens = message.split(" ", 1)
        if tokens[0] == 'iWant':
            fileName = tokens[1]
            new_path = raw_input('Directory:')
            if new_path != '':
                path = new_path
            path = path + fileName
            fileMessage = clientSocket.recv(1024)
            test = fileMessage.split(":", 1)
            if test[0] == "Failure":
                print fileMessage
            else:
                f = open(path, 'wb')
                while fileMessage:
                    f.write(fileMessage)
                    fileMessage = clientSocket.recv(1024)
                print 'Receive complete.'
                f.close()
            break
        elif tokens[0] == 'uTake':
            sendFile(clientSocket, tokens[1])
            clientSocket.shutdown(SHUT_WR)
            print 'Send Complete'
            break
        else:
            print ('That just ain\'t right! Bad command: '+ message)
    clientSocket.close()

def sendFile(sock, fileName):
    path = './received/' + fileName
    if not os.path.isfile(path):
        message = 'Failure: What you talkin\' bout Willis?  I ain\'t seen that file nowhere!'
        sock.send(message)
        print message
        return
    f = open(path, 'rb')
    l = f.read(1024)
    while l:
        sock.send(l)
        l = f.read(1024)
    f.close()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        clientSocket.shutdown(SHUT_RDWR)
        clientSocket.close()
