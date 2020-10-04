##Reverse Shell

A reverse shell is a shell session established on a connection that is initiated from a remote machine, not from the local host. Attackers who successfully exploit a remote command execution vulnerability can use a reverse shell to obtain an interactive shell session on the target machine and continue their attack.

The following repository contains 2 files the server and the client. The server file is used by the hacker to give commands to the remote pc. The client file resides on the victims system and is used to establish the connection between the two.

To run the program in the local machine change the IP Address in the client file to the IP Address of your lan

The IP Address of the LAN can be found out using : ```ipconfig``` in Windows and ```ifconfig``` in Linux

To run the program in public network upload the server file onto your server and change the IP Address in the client file to your server's IP Address

