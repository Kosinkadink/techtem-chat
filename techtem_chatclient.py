#!/usr/bin/python2
import sys
import socket
import select
 
def chat_client():

	host = 'localhost'
	port = 9009
	 
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.settimeout(2)
	 
	# connect to remote host
	try :
		s.connect((host, port))
	except :
		print 'Unable to connect'
		sys.exit()
	
	print 'Connected to remote host. You can start sending messages'
	
	#request information
	name = raw_input("Name (optional):")
	if name == "":
		tripcode = ""
	else:
		tripcode = raw_input("Tripcode (also optional):")

	sys.stdout.write("[" + name + "]"); sys.stdout.flush()
 
	while 1:
		socket_list = [sys.stdin, s]
		 
		# Get the list sockets which are readable
		ready_to_read,ready_to_write,in_error = select.select(socket_list , [], [])
		 
		for sock in ready_to_read:			 
			if sock == s:
				# incoming message from remote server, s
				data = sock.recv(4096)
				if not data :
					print '\nDisconnected from chat server'
					sys.exit()
				else :
					#print data
					sys.stdout.write(data)
					sys.stdout.write('\n[' + name + '] '); sys.stdout.flush()	 
			
			else :
				# user entered a message
				message = sys.stdin.readline()
				if message[0] == "/":
					if message.split()[0] == "/changename":
						name = raw_input("New name: ")
					if message.split()[0] == "/changetripcode":
						tripcode = raw_input("New tripcode: ")
				else:
					data = message + name + "\n" + tripcode
					s.send(data)
				sys.stdout.write('[' + name + '] '); sys.stdout.flush() 

if __name__ == "__main__":

	sys.exit(chat_client())
