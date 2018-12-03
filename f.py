# -*- coding: utf-8 -*-
import asyncore
import socket
import sys
class forwarder(asyncore.dispatcher):
    print("-----------C: forwarder---------------")
    def __init__(self, ip, port, rip, rport, tip, tport, backlog=5):
        asyncore.dispatcher.__init__(self)
        self.rip = rip
        self.rport = rport
        self.tip = tip
        self.tport = tport

        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.set_reuse_addr()
        self.bind((ip, port))
        self.listen(backlog)

    def handle_accept(self):
        con, addr = self.accept()
        print("Connetced to" + str(addr))
        # data = con.recv(8096)
        # data_str = str(data, encoding='utf-8')
        # link = data_str.split('\r\n')
        # link =  link[0].split()
        # link = link[1]
        # print(link)
        # con.send(data)
        # if link == '/other/':
        #     sender(receiver(con), self.tip, self.tport)
        # elif link == '/':
        #     sender(receiver(con), self.rip, self.rport)
        sender(receiver(con), self.rip, self.rport)


class sender(asyncore.dispatcher):
    print("-----------C: sender---------------")
    def __init__(self, receiver, raddr, rport):
        asyncore.dispatcher.__init__(self)
        self.receiver = receiver()
        receiver.sender = self
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect((raddr, rport))
        # sys.stdout.flush()

    def handle_connect(self):
        pass

    def handle_read(self):
        read = self.recv(4096)
        print(read)
        self.receiver.to_remote_buffer += read

    def writeable(self):
        return (len(self.receiver.from_remote_buffer)>0)

    def handle_write(self):
        sent = self.send(self.receiver.from_remote_buffer)
        self.receiver.to_remote_buffer = self.receiver.from_remote_buffer[sent:]

    def handle_close(self):
        self.close()
        self.receiver.close()

class receiver(asyncore.dispatcher):
    print("-----------C: receiver---------------")
    def __init__(self, conn):
        asyncore.dispatcher.__init__(self,conn)
        self.from_remote_buffer = ''
        self.to_remote_buffer = ''
        self.sender = None

    def handle_connect(self):
        print("-----------D: handle_connect---------------")
        pass

    def handle_read(self):
        read = str(self.recv(4096))
        print(read.encode('utf-8'))
        self.from_remote_buffer += read

    def writable(self):
        return (len(self.to_remote_buffer) > 0)

    def handle_write(self):
        sent = self.send(self.to_remote_buffer)
        self.to_remote_buffer = self.to_remote_buffer[sent:]

    def  handle_close(self):
        self.close()
        if self.sender:
            self.sender.close()

if __name__ == '__main__':
    ip = '127.0.0.1'
    port = 8000
    rip = '192.168.7.97'
    tip = '192.168.7.97'
    rport = 81
    tport = 7004

    s = forwarder(ip=ip, port=port, rip=rip, rport=rport, tip=tip ,tport=tport)
    # t = forwarder(ip=tip, port=port, rip=rip, rport=rport)
    asyncore.loop()
