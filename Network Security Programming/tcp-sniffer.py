# TCP packet sniffer using raw sockets
# Usage: sudo python2 tcp-sniffer.py

import socket
import struct
import binascii
import ctypes


c_uint8 = ctypes.c_uint8


class Tcp_flags_bits(ctypes.LittleEndianStructure):
	_fields_ = [
		("C",	c_uint8, 1),
		("E",	c_uint8, 1),
		("U",	c_uint8, 1),
		("A",	c_uint8, 1),
		("P",	c_uint8, 1),
		("R",	c_uint8, 1),
		("S",	c_uint8, 1),
		("F",	c_uint8, 1)
	]

class Tcp_flags(ctypes.Union):
	_fields_ = [
		("b",		Tcp_flags_bits),
		("asByte",	c_uint8)
	]
	_anonymous_ = ("b")

big_line = "================================================================"

rawSocket = socket.socket(socket.PF_PACKET, socket.SOCK_RAW, socket.htons(0x0800))

while True:
	pkt = rawSocket.recvfrom(2048)


	raw_ip_header = pkt[0][14:34] 


	ip_header = struct.unpack("!B8sB2s4s4s", raw_ip_header)

	protocol = ip_header[2]
	if protocol != 6:
		continue
	ihl = (ip_header[0] & 0x0F)*4
	
	print big_line
	print "[IP] Source: " + socket.inet_ntoa(ip_header[4]),
	print ", Destination: " + socket.inet_ntoa(ip_header[5])


	raw_tcp_header = pkt[0][14+ihl:54] 

	
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
	reserved = tcp_header[4] & 0x0F	
	flags = Tcp_flags()
	flags.asByte = tcp_header[5]	
	window_size = tcp_header[6]	
	checksum = tcp_header[7]	
	urgent_pointer = tcp_header[8]

	print "Source Port: " + str(src_port)
	print "Destination Port: " + str(dst_port)
	print "Sequence Number: " + str(seq_num)
	print "Acknowledgement number: " + str(ack_num)
	print "Header length: " + str(offset) + " bytes"
	print "Reserved: " + "{0:b}".format(reserved)
	print "Flags: "
	print "  " + str(flags.C) + "....... Congestion Window Reduced (CWR)"
	print "  ." + str(flags.E) + "...... ECN Echo (ECE)"
	print "  .." + str(flags.U) + "..... Urgent"
	print "  ..." + str(flags.A) + ".... Ack"
	print "  ...." + str(flags.P) + "... Push"
	print "  ....." + str(flags.R) + ".. Reset"
	print "  ......" + str(flags.S) + ". Syn"
	print "  ......." + str(flags.F) + " Fin"
	print "Window size: " + str(window_size)
	print "Checksum: " + "0x{:04X}".format(checksum)


	if offset > 20:
		options_size = offset - 20
		raw_tcp_options = pkt[0][54:54+options_size]
		print "TCP Options: " + "".join(c.encode('hex') for c in raw_tcp_options)
		
		i = 0
		while i < len(raw_tcp_options):
			kind = raw_tcp_options[i]
			if kind == "\x01":
				print "  NOP"
			elif kind == "\x08":
				length = raw_tcp_options[i+1] 
				ts_val = struct.unpack("I", raw_tcp_options[i+2:i+6])[0]
				ts_ecr = struct.unpack("I", raw_tcp_options[i+6:i+10])[0]
				print "  Timestamp"
				print "    TSval: " + str(ts_val)
				print "    TSecr: " + str(ts_ecr)
				i += 9
			i += 1
