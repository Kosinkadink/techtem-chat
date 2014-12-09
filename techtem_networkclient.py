#!/usr/bin/python2
import sys
import socket
import select

def net_client():
	print "========================================================="
	print "Welcome to the TechTem Network Client"
	print "Version 0.01"
	print "Type /help for command list"
	while 1:
		inp = raw_input("> ")
		if inp[0] == '/':
			if inp.split()[0] == '/connect':
				sys.stdout.write(retrieveip(inp.split()[1]))
				sys.stdout.flush()
			elif inp.split()[0] == '/dconnect':
				print "Work in progress, not available"
			elif inp.split()[0] == '/quit' or inp.split()[0] == '/leave':
				quit() 
			elif inp.split()[0] == '/help' or inp.split()[0] == '/?':
				print "TechTem Network Client Commands:\n/connect + URL: retrieve address and connect\n/dconnect + IP: directly connect to IP\n/quit OR /leave: exits gracefully\n/help OR /?: displays this menu"
			else:
				print "Invalid command"

def retrieveip(url):
	host = 'localhost'
	port = 9010

	# create a socket object
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)                           

	# connection to hostname on the port.
	s.connect((host, port))                               

	s.send(url)
	# Receive no more than 1024 bytes
	ip = s.recv(1024)                                    

	s.close()

	return ip

def connectip(ip):
	pass
 
def chat_client(h,p):

	try:
		host = h
		port = p
	except:
		print 'Incorrect syntax'
		sys.exit()
	# paste client code here 
	

if __name__ == "__main__":

	sys.exit(net_client())
