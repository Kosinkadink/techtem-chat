#!/usr/bin/python2
import sys, socket, select, os
from JedEncryptM import JedEncrypt
from time import strftime

f = JedEncrypt()

HOST = '' 
SOCKET_LIST = []
RECV_BUFFER = 4096 
PORT = 9010

def date():
	return strftime("%Y-%m-%d")

def time():
	return strftime("%H:%M:%S")

def localLog(a):
	print a
	log = open(date(), "a")
	log.write(time() + " " + a + "\n")
	log.close

def searchurls(rqst):
	ip = '404\n'
	with open("techtemurls") as file:
		for line in file:
			url = line.split("||")
			if url[0] == rqst:
				ip = url[1]
				break
	return ip

def net_server():
	# create a socket object
	serversocket = socket.socket(
				socket.AF_INET, socket.SOCK_STREAM) 

	# get local machine name
	host = socket.gethostname()						   
	port = 9010										   

	# bind to the port
	serversocket.bind((host, port))								  

	# queue up to 10 requests
	serversocket.listen(10)										   

	while 1:
		# establish a connection
		clientsocket,addr = serversocket.accept()
		print("Got a connection from %s" % str(addr))
		rqst = clientsocket.recv(1024)
		message = searchurls(rqst)
		clientsocket.send(message)
		clientsocket.close()
		print("Disconnection by %s with data received" % str(addr))
	serversocket.close()

if __name__ == "__main__":

	sys.exit(net_server())
