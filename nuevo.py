#!/user/bin/python3

import sys, socket, re, os, string, time



class mk_socket:
    
    def __init__(self, host, port=21):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((host, port))
        self.open = True
		
	def send(self, mes=''):
        self.s.send(mes + '\r\n')

		
class ftp_client:
    def __init__(self):
        self.timezone = 0
        self.buffer_size = 1024
    
	 def connect(self, host):
        self.sock_main = mk_socket(host)

     def LOGIN(self, usern, passw):
		self.sock_main.send('USER '+usern)
		self.sock_main.send('PASS '+passw)
		 

if __name__ == '__main__':
    
	MYclient = ftp_client()
	
	MYclient.connect(raw_input("Direccion: "))
	
	MYclient.LOGIN(raw_input("Username: "),
                       raw_input("Password: "))
	print ("login")
		
