import socket
import SimpleHTTPServer
import SocketServer
from scapy.all import *
from subprocess import Popen

exit_node_ip = None
only_once = True

class MyHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    def handle_one_request(self):
        print(self.client_address[0])
        exit_node_ip = self.client_address[0]
        global only_once
        if only_once:
            only_once = False
            proc = Popen("python pkts_to_attkr.py " + str(exit_node_ip), shell=True, stdin=None, stdout=None, stderr=None, close_fds=True)
        return SimpleHTTPServer.SimpleHTTPRequestHandler.handle_one_request(self)

print("Serving local directory")
SocketServer.TCPServer.allow_reuse_address = True
httpd = SocketServer.TCPServer(("", 8003), MyHandler)

while True:
    httpd.handle_request()
