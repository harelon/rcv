import socket
import errno
import json
from time import sleep

def send_data():
    global connection_available
    data ={
        "p1": {"d": 50.9, "a": 23},
        "p2": {"d": 60, "a": 27}
    }
    json_string = json.dumps(data)
    try:
        client_socket.sendall(json_string)
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
        return False
    else:
        print("connected succesfully")
        return True


def connect_and_send():
    global connection_available
    if not connection_available:
        connection_available = establish_connection()
    if connection_available:
        send_data()
    sleep(1)


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
