#!/usr/bin/python2
import sys, socket, select, os
from JedEncryptM import JedEncrypt
from datetime import datetime
from random import randint
from time import sleep

f = JedEncrypt()

HOST = '' 
SOCKET_LIST = []
RECV_BUFFER = 4096 
PORT = 9009

maliciouswords = []
#read maliciouswords file and append each line to the list of malicious words
if os.path.isfile("maliciouswords"):
	with open("maliciouswords", "r") as maliciouswordsfile:
		for line in maliciouswordsfile:
			maliciouswords.append(line.replace("\n",""))


def date():
	return datetime.now().strftime("%Y-%m-%d")

def timestamp():
        return "<{}> ".format(datetime.now().strftime("%H:%M:%S.%f"))

def chat_server():

	server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	server_socket.bind((HOST, PORT))
	server_socket.listen(10)
	display="" 
	# add server socket object to the list of readable connections
	SOCKET_LIST.append(server_socket)

        addrlist = [HOST]
	log = open(date(), "a")
	log.write(timestamp() + "Server has started.\n")
	log.close


	while 1:
                sleep(.1)
		# get the list sockets which are ready to be read through select
		# 4th arg, time_out  = 0 : poll and never block
		ready_to_read,ready_to_write,in_error = select.select(SOCKET_LIST,[],[],0)

		for sock in ready_to_read:
			# a new connection request recieved
			if sock == server_socket:
                                #This is partially a placeholder variable, but also makes sense because the current socet is the server socket
				sockfd, addr = server_socket.accept()
				SOCKET_LIST.append(sockfd)
                                addr = addr[0]
                                #because the IP and socket are appended to their corresponding lists at the same time, they will share the same index value
				addrlist.append(addr)
                                #turn the sock ID into a 4-digit string to make it easier to read from the log
				broadcast(server_socket, addr, "Someone has entered the chat. There is currently {} people in the chatroom.".format(len(SOCKET_LIST)-1))
			# a message from a client, not a new connection
			else:
                                #figure out what the IP is for the sending client
				addr = addrlist[SOCKET_LIST.index(sock)]
    			        # process data recieved from client
				try:
					# receiving data from the socket.
					data = sock.recv(RECV_BUFFER)
				except:
					broadcast(server_socket, addr, "Someone has disconnected. There is currently {} people in the chatroom.".format(len(SOCKET_LIST)-1))
					continue
				if data:
					# there is something in the socket
					#find the message, if any
					message = data.splitlines()[0]
					if message:
						if message[0] == "/":
							isCommand = True
							command = message.split()[0]
						else:
							isCommand = False

						#find the name, if any
						try:
							name = data.splitlines()[1]
							if name == "":
								name = "Anonymous"
						except:
							name = "Anonymous"
						try:
							#find and hash the tripcode
							tripcode = data.splitlines()[2]
							if tripcode:
								f.key(tripcode)
								hsh = f.encrypt(tripcode)
							else:
								hsh = ""
						except:
							hsh = ""
						if hsh:
							hsh = " {{{}}}".format(hsh)
						#format all information into readable stuff
						if message.lower() not in maliciouswords:
							display = "[{}]{}: {}".format(name, hsh, message)
						else:
							display = name + " has said malicious words."
						if not isCommand:
							broadcast(server_socket, addr, display)
						elif command == "/pm":
                                                        #find the parameter of the command (the phrase being scanned for in the timestamp)
                                                        try:
                                                                target = message.split()[1]
                                                        except:
                                                                #if there is no parameter, make it something that will definitely be invalid
                                                                target = "invalid"
                                                        #find that timestamp in the log
			                                targetaddr = None
							with open(date(), "r") as log:
                                                                for line in log:
                                                                        if target in line.split()[0]:
                                                                                #find the addr associated with that timestamp
										targetaddr = line.split()[-1]
							if targetaddr:
                                                                #send the junk to the target
                                                                tobesent = "{}##pm## [{}]{}: {}".format(timestamp(), name, hsh, message[len(target) + 5:])
                                                                SOCKET_LIST[addrlist.index(targetaddr)].send(tobesent)
                                                                with open(date(), "a") as log:
                                                                        log.write("{} [sent to ID: {}] {}\n".format(tobesent, targetaddr, addr))
							else:
								sock.send("Invalid target")
                                                elif command == "/peoplecount":
                                                        sock.send("There is currently {} people in the chatroom.".format(len(SOCKET_LIST)-1))
				else:
					# remove the socket that's broken
					if sock in SOCKET_LIST:
						addrlist.remove(addrlist[SOCKET_LIST.index(sock)])
						SOCKET_LIST.remove(sock)
						# at this stage, no data means probably the connection has been broken
						broadcast(server_socket, addr, "Someone has disconnected. There is currently {} people in the chatroom.".format(len(SOCKET_LIST)-1))

	server_socket.close()
    
# broadcast chat messages to all connected clients
def broadcast (server_socket, addr, message):
        tobesent = timestamp() + message
	for socket in SOCKET_LIST:
		# send the message only to peer
		if socket != server_socket:
			try :
				socket.send(tobesent)
			except :
				# broken socket connection
				socket.close()
				# broken socket, remove it
				if socket in SOCKET_LIST:
					SOCKET_LIST.remove(socket)
	log = open(date(), "a")
	log.write(tobesent + " " + addr + "\n")
	log.close

if __name__ == "__main__":

	sys.exit(chat_server())
