import socket

s = socket.socket()
host = socket.gethostname()
port = 90
s.bind((host,port))

s.listen(5)
while True:
    c, addr = s.accept()
    print("Got connnect from:" + str(addr))
    c.send('Thank you for connecting!')
    # c.close()
