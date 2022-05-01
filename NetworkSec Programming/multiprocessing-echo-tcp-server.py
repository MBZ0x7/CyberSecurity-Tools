# TCP Echo back server using multiprocessing which accept more than one client

import socket
import sys
from multiprocessing import Process

def EchoClientHandler(clientSocket, addr) :
	while 1:
		client_data  = clientSocket.recv(2048)
		if client_data :
			clientSocket.send(client_data)
		else :
			clientSocket.close()
			return



echoServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

echoServer.bind(("127.0.0.1", 1337))

echoServer.listen(2)

workerProcesses = []

while 1:
	cSock, addr = echoServer.accept()
	print ("Starting a new process to service new client...\n")
	worker = Process(target=EchoClientHandler, args= (cSock, addr))
	worker.start()
	workerProcesses.append(worker)
