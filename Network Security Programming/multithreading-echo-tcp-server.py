# TCP Echo back server using multithreading which accept more than one client (here we defined 10)

import signal
import socket
import threading

tcpSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

HOST = "127.0.0.1"
PORT = 1338
tcpSocket.bind((HOST, PORT))
tcpSocket.listen(1)

class WorkerThread(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)

	def run(self):
		while True:
			(client, addr) = tcpSocket.accept()
			print("Got Connection From: ", addr)

			client.send(b"Connection Established!\n")
			data = client.recv(2048)
			while data:
				client.send(data)
				data = client.recv(2048)

print("Starting server...")
for i in range(10):
	worker = WorkerThread()	
	worker.setDaemon(True)
	worker.start()

def exit_handler(signum, frm):
	print("Terminating...")
	exit()
	
signal.signal(signal.SIGINT, exit_handler)

while True:
	pass
