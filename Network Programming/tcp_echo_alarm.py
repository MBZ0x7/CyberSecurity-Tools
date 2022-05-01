# A TCP echo server that shuts down after X seconds using alarm signal
# Usage: tcp_echo_alarm.py -s <nb_seconds>

import sys
import socketserver
import signal

class TcpHandler(socketserver.BaseRequestHandler):
  def setup(self):
    print("Got Connection From {}".format(self.client_address[0]))

  def handle(self):
    self.data = self.request.recv(1024).strip()
    print("{} Wrote:".format(self.client_address[0]))
    print(self.data)
    self.request.sendall(self.data)


def alarm_handler(signum, frm):
  print("Terminating...")
  exit()

if len(sys.argv) != 3 or sys.argv[1] != "-s":
  print("Usage: tcp_echo_alarm.py -s <nb_seconds>") 
  exit()

timeout = int(sys.argv[2])
signal.signal(signal.SIGALRM, alarm_handler)
signal.alarm(int(timeout))

print("Starting server...")
socketserver.TCPServer.allow_reuse_address = True
server = socketserver.TCPServer(('127.0.0.1', 1337), TcpHandler)
server.serve_forever()
