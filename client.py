import socket

def c ():
    s =socket.socket()

    host = socket.gethostname()
    port = 90
    s.connect((host, port))
    print(s.recv(1024))

if __name__ == '__main__':
    for i in range(1,20):
        print(i)
        c()