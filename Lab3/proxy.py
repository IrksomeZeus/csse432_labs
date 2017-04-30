from socket import *

import thread
import sys
import re

MAX_THREADS = 5
Num_Threads = 0
Server_Socket = ''


def main():
    global Server_Socket
    global Num_Threads
    port = int(sys.argv[1])
    host = '127.0.0.1'
    Server_Socket = socket(AF_INET, SOCK_STREAM)
    Server_Socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    Server_Socket.bind((host, port))
    Server_Socket.listen(1)
    print 'The server has started\nHost ' + host + ' Port ' + str(port)
    while True:
        connection, addr = Server_Socket.accept()
        if Num_Threads < MAX_THREADS:
            thread.start_new_thread(client, (connection, addr))
            Num_Threads += 1
            print 'Thread Created. Num Threads: ' + str(Num_Threads)
        else:
            connection.close()


def client(client_socket, addr):
    global Num_Threads
    client_request = ''
    while True:
        ch = client_socket.recv(1024)
        if len(ch) == 0:
            print 'Closing Client.'
            break
        client_request = client_request + ch
        if client_request[-2:] == '\r\n':
            print client_request
            if check_request(client_request):
                # TODO open socket and send request to destination server
            else:
                # TODO send bad request message
            client_request = ''
    client_socket.close()
    Num_Threads -= 1
    print 'Thread closed. Num Threads: ' + str(Num_Threads)


def check_request(request):
    lines = request.splitlines(True)
    if not valid_http(lines[1]):
        return False
    for line in lines[2:]:
        if not valid_header(line):
            return False
    return True


def valid_http(text):
    http_pattern = re.compile("([A-Z])+[ ]([\w\d.-])+:[0-9]+[ ]HTTP\/[\d.]+\r\n")
    return http_pattern.match(text)


def valid_header(text):
    header_pattern = re.compile("(.[^ ])+: (.[^ ])+\r\n")
    return header_pattern.match(text)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        Server_Socket.close()
        sys.exit(1)
