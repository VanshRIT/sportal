import socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = socket.gethostname()
port = 8888

s.connect((host, port))
while True:
    msg=input("enter message")

    s.send(msg.encode("utf-8"))

    if msg==".":
        break
    msg=s.recv(2024)
    print (msg.decode('utf-8'))