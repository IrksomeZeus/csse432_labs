# Douglas Wise and Austin Yates
# CSSE432 Computer Networks - Lab 2
# March 31, 2017

from socket import *
import os.path
serverPort = 12000
serverSocket = 0

def main():
    global serverSocket
    serverSocket = socket(AF_INET, SOCK_STREAM)
    serverSocket.bind(('',serverPort))
    serverSocket.listen(1)
    print "The server has started.\nUse ctrl-c to quit."
    while 1:
        connectionSocket, addr = serverSocket.accept()
        clientInput = connectionSocket.recv(1024)
        tokens = clientInput.split(' ', 1)
        command = tokens[0]
        if command == 'iWant':
            print 'Request received for ' + tokens[1]
            sendFile(connectionSocket, tokens[1])
            connectionSocket.shutdown(SHUT_WR)
        elif command == 'uTake':
            path = './store/'
            fileName = tokens[1]
            new_path = raw_input('Save Directory (default is ./store/):')
            if new_path != '':
                path = new_path
            print 'Saving ' + fileName + ' to ' + path
            path = path + fileName
            fileMessage = connectionSocket.recv(1024)
            test = fileMessage.split(":", 1)
            if test[0] == "Failure":
                print fileMessage
            else:
                f = open(path, 'wb')
                while fileMessage:
                    f.write(fileMessage)
                    fileMessage = connectionSocket.recv(1024)
                print 'Receive complete.'
                f.close()
        else:
            print ('That just ain\'t right! Bad command: '+ clientInput)
            connectionSocket.send('That just ain\'t right!')
        connectionSocket.close()

def sendFile(sock, fileName):
    path = './store/' + fileName
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
        print 'Closing.'
        serverSocket.shutdown(SHUT_RDWR)
        serverSocket.close()
