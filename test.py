import asyncore
import socket


class forwarder(asyncore.dispatcher):

    def __init__(self, ip, port, rip, rport, backlog=5):
        asyncore.dispatcher.__init__(self)
        self.rip = rip
        self.rport = rport
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.set_reuse_addr()
        self.bind((ip, port))
        self.listen(backlog)

    def handle_accept(self):
        conn, addr = self.accept()
        sender(receiver(conn), self.rip, self.rport)


class sender(asyncore.dispatcher):

    def __init__(self, rip, rport, receiver):
        asyncore.dispatcher.__init__(self)
        self.receiver = receiver
        self.sender = self
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect((rip, rport))

    def handle_connect(self):
        pass

    def handle_read(self):
        read = self.recv(1024)
        self.receiver.from_remote_buffer = self.receiver.from_remote_buffer[sent:]

    def handle_close(self):
        self.close()
        self.receiver.close()

class receiver(asyncore.dispatcher):

    def __init__(self, conn):
        asyncore.dispatcher.__init__(self)
        self.from_remote_buffer = ''
        self.to_remote_buffrt = ''
        self.sender = None

    def handle_connect(self):
        pass

    def handle_read(self):
        read = self.recv(1024)
        self.from_remote_buffer += read


    def writable(self):
        return (len(self.to_remote_buffrt) >  0)

    def handle_write(self):
        sent = self.send(self.to_remote_buffrt)
        self.to_remote_buffrt = self.to_remote_buffrt[sent:]

    def handle_close(self):
        self.close()
        if self.sender:
            self.sender.close()


if __name__ == '__main__':
    ip = '127.0.0.1'
    port = 8000
    tip = '192.168.7.97'
    tport = 7300

    forwarder(ip , port, tip, tport)
    asyncore.loop()