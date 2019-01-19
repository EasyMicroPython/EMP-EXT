import gc
import json
import os
import socket
import sys

import _webrepl
import emp_wifi
import network
import websocket
import websocket_helper


class WebREPL:

    def __init__(self):
        self.ws = None
        self.listen_s = None
        self.client_s = None
        self.wr = None

    def send(self, json_data):
        self.ws.write(json_data)

    def setup_conn(self, port, accept_handler):
        self.listen_s = socket.socket()
        self.listen_s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        ai = socket.getaddrinfo("0.0.0.0", port)
        addr = ai[0][4]

        self.listen_s.bind(addr)
        self.listen_s.listen(1)
        if accept_handler:
            self.listen_s.setsockopt(socket.SOL_SOCKET, 20, accept_handler)
        for i in (network.AP_IF, network.STA_IF):
            iface = network.WLAN(i)
            if iface.active():
                print(rainbow("WebREPL daemon started on ws://%s:%d" %
                              (iface.ifconfig()[0], port), color='green'))
        return self.listen_s

    def accept_conn(self, listen_sock):

        cl, remote_addr = listen_sock.accept()
        prev = os.dupterm(None)
        os.dupterm(prev)
        if prev:
            print("\nConcurrent WebREPL connection from",
                  remote_addr, "rejected")
            cl.close()
            return
        print("\nWebREPL connection from:", remote_addr)
        self.client_s = cl
        websocket_helper.server_handshake(cl)
        self.ws = websocket.websocket(cl, True)

        self.wr = _webrepl._webrepl(self.ws)
        type(self.wr)
        cl.setblocking(False)
        # notify REPL on socket incoming data
        cl.setsockopt(socket.SOL_SOCKET, 20, os.dupterm_notify)
        os.dupterm(self.wr)

    def stop(self):
        os.dupterm(None)
        if self.client_s:
            self.client_s.close()
        if self.listen_s:
            self.listen_s.close()

    def start(self, port=8266, password=None):
        self.stop()
        if password is None:
            try:
                import webrepl_cfg
                _webrepl.password(webrepl_cfg.PASS)
                self.setup_conn(port, self.accept_conn)
                print("Started webrepl in normal mode")
            except:
                print("WebREPL is not configured, run 'import webrepl_setup'")
        else:
            _webrepl.password(password)
            self.setup_conn(port, self.accept_conn)
            print(rainbow("WebREPL started.", color='green'))

    def start_foreground(self, port=8266):
        self.stop()
        s = self.setup_conn(port, None)
        self.accept_conn(s)
