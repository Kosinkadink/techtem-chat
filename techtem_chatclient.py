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
	
	print 'Connected to remote host.'
	
	#request information
	name = raw_input("Name (optional): ")
	if name == "":
		tripcode = ""
	else:
		tripcode = raw_input("Tripcode (also optional): ")

	sys.stdout.write("\n[" + name + "] "); sys.stdout.flush()
 
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
					sys.stdout.write("\r") # brings cursor to the beginning of the line, probably skips line
					sys.stdout.write("\033[F") # brings cursor up one line, where the old text is now
					sys.stdout.write('\n' + data) # skips line (due to change with server), writes data on top of old text
					sys.stdout.write('\n[' + name + '] ') # skips to new first line, rewrites name
					sys.stdout.flush()	 
			
			else :
				# user entered a message
				message = sys.stdin.readline()
				if message[0] == "/":
					#that message was a command
					if message.split()[0] == "/changename": 
						name = message[len(message.split()[0])+1:].replace("\n","")
					elif message.split()[0] == "/changetripcode":
						tripcode = message[len(message.split()[0])+1:].replace("\n","")
					elif message.split()[0] == "/quit" or message.split()[0] == "/leave":
						quit()
					elif message.split()[0] == "/help" or message.split()[0] == "/?":
						sys.stdout.write("\nThanks for using the techtemchat client. Here are the commands you currently have available:\n/changename + new name: changes your name\n/changetripcode + new tripcode: changes your trip code.\n/quit OR /leave: exits gracefully\n/help OR /?: Displays this menu.\n")
					else:
						print "Invalid command"
				else:
					data = message + name + "\n" + tripcode
					s.send(data)
				sys.stdout.write('[' + name + '] ')
				sys.stdout.flush() 

if __name__ == "__main__":

	sys.exit(chat_client())
