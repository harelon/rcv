import socket
import errno
import json
from time import sleep
from combine_modules import get_data, init


def send_data():
    global connection_available
    data = get_data()
    try:
        client_socket.sendall(data)
    except socket.error as e:
        print(e)
        print(e.errno)
        client_socket.close()
        connection_available = False
        if e == socket.timeout:
            print("connection is unavailable retrying to connect")
        else:
            print(e.errno)


def init_socket():
    global client_socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.settimeout(1)


def establish_connection():
    init_socket()
    err = client_socket.connect_ex((ip, port))
    if err == socket.error:
        print(str(err) + " connection error")
        print("connection timed out")
        exit()
    if err != 0:
        client_socket.close()
        print("couldn't connect")
        return False
    else:
        print("connected succesfully")
        init()
        return True


def connect_and_send():
    global connection_available
    if not connection_available:
        connection_available = establish_connection()
    if connection_available:
        send_data()


def main():
    global ip
    global port
    global connection_available
    ip = '192.168.3.5'
    port = 8083
    connection_available = False
    while True:
        connect_and_send()


if __name__ == '__main__':
    main()
