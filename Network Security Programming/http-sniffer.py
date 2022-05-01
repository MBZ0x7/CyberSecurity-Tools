# HTTP packet sniffer using raw sockets
# Usage: sudo python2 http-sniffer.py

import socket
import binascii
import struct

ETH_LEN = 14
big_line = "================================================================"
small_line = "----------------------------------------------------------------"

rawSocket = socket.socket(socket.PF_PACKET, socket.SOCK_RAW, socket.htons(0x0800))

while True:
	pkt = rawSocket.recvfrom(2048)


	raw_ip_header = pkt[0][ETH_LEN:34]


	ip_header = struct.unpack("!B8sB2s4s4s", raw_ip_header)

	protocol = ip_header[2]	
	if protocol != 6:
		continue
	ihl = (ip_header[0] & 0x0F)*4	
	

	raw_tcp_header = pkt[0][ETH_LEN+ihl:ETH_LEN+ihl+20]


	try:
		tcp_header = struct.unpack("!HHIIBBHHH", raw_tcp_header)
	except struct.error:
		print "Error while attempting to unpack tcp header!"
		print "".join(c.encode('hex') for c in raw_tcp_header)
		continue

	src_port = tcp_header[0]	
	dst_port = tcp_header[1]	
	seq_num = tcp_header[2]		
	ack_num = tcp_header[3]		
	offset = (tcp_header[4] >> 4)*4

	if not src_port == 80 and not dst_port == 80:
		continue


	http_payload = pkt[0][ETH_LEN+ihl+offset:]

	print big_line
	print "[IP] Source: " + socket.inet_ntoa(ip_header[4]),
	print ", Destination: " + socket.inet_ntoa(ip_header[5])
	print "Source Port: " + str(src_port)
	print "Destination Port: " + str(dst_port)
	print "Sequence Number: " + str(seq_num)
	print "Acknowledgement number: " + str(ack_num)
	print small_line
	print http_payload
	print small_line
