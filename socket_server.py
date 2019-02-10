import socket


s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server="192.168.3.114"
port=8083
s.bind((server,port))
s.listen(5)
while True:
    conn,addr=s.accept()
    while True:
        data = conn.recv(1024)
        if data is None:
            break
        print(data.decode("utf-8"))