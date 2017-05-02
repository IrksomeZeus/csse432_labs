#! /usr/bin/env python
import re
import sys
import thread
from socket import *

MAX_THREADS = 100
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
    while True:
        connection, addr = Server_Socket.accept()
        if Num_Threads < MAX_THREADS:
            thread.start_new_thread(client, (connection, addr))
            Num_Threads += 1
        else:
            connection.close()


def client(client_socket, addr):
    global Num_Threads
    client_request = ''
    while True:
        ch = client_socket.recv(1024)
        if len(ch) == 0:
            break
        client_request = client_request + ch
        if client_request[-2:] == '\r\n':
            lines = client_request.splitlines(True)
            if check_request(lines):
                line = lines[0]
                method, url, http = line.split(' ')
                url = url[7:]
                domain, value = url.split('/', 1)
                value = '/' + value
                connection = 'Connection: close\r\n'

                if not method == 'GET':
                    client_socket.sendall("Not Implemented (500)")
                    client_socket.close()
                    Num_Threads -= 1
                    return

                request = method + ' ' + value + ' ' + http

                first = True
                if len(lines) == 1:
                    request = request + 'Host: ' + domain + '\r\n'
                for line in lines[1:]:
                    if line == '\r\n':
                        first = False
                        continue
                    word, rest = line.split(' ', 1)
                    if first:
                        if word == 'Host:':
                            request = request + line
                            first = False
                            continue
                        else:
                            first = False
                            request = request + 'Host: ' + domain + '\r\n'
                    if not 'Connection:' == word and not 'Upgrade-Insecure-Requests' == word:
                        request = request + line

                request = request + connection + '\r\n'
                dest_socket = socket(AF_INET, SOCK_STREAM)
                domain = gethostbyname(domain)
                dest_socket.connect((domain, 80))
                dest_socket.sendall(request)
                while True:
                    data = dest_socket.recv(4096)
                    if len(data) == 0 or data == '':
                        break
                    else:
                        client_socket.sendall(data)
                break
            else:
                client_socket.sendall("Bad Request (400)")
                client_socket.close()
                Num_Threads -= 1
                return
            client_request = ''
    client_socket.close()
    Num_Threads -= 1


def check_request(lines):
    if not valid_http(lines[0]):
        return 'Bad Request'
    for line in lines[1:]:
        if not valid_header(line):
            return 'Bad Request'
    return 'Good'


def valid_http(text):
    http_pattern = re.compile("([A-Z])+ (http|HTTP):\/\/[^\s]+ HTTP\/1.0\r\n")
    if http_pattern.match(text):
        return True
    else:
        return False


def valid_header(text):
    if text == '\r\n':
        return True
    header_pattern = re.compile("([^\s])+: .+\r\n")
    if header_pattern.match(text):
        return True
    else:
        return False


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        Server_Socket.close()
        sys.exit(1)
