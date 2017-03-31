from socket import *
serverPort = 12000
serverSocket = 0

def main():
    global serverSocket
    serverSocket = socket(AF_INET, SOCK_STREAM)
    serverSocket.bind(('',serverPort))
    serverSocket.listen(1)
    print "The server is ready to receive."
    while 1:
        connectionSocket, addr = serverSocket.accept()
        clientInput = connectionSocket.recv(1024)
        tokens = clientInput.split(' ', 1)
        command = tokens[0]
        if command == 'iWant':
            connectionSocket.send('Request received for ' + tokens[1])
            print 'Request received for ' + tokens[1]
        elif command == 'uTake':
            pass
        else:
            print ('That just ain\'t right! Bad command: '+ clientInput)
            connectionSocket.send('That just ain\'t right!')
        connectionSocket.close()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print 'Closing.'
        serverSocket.shutdown(SHUT_RDWR)
        serverSocket.close()
