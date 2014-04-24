#!/user/bin/python3

import sys, socket, re, os, string, time, urllib2

class mk_socket:
    
    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((192.100.230.21, 21))
        self.sid = str(sid)
        self.open = True
        
     def relay(self, mes='', expect=False, filt=''):
        self.send(mes, True, filt)
        return self.recv(expect)

    def recv(self, expect=False):
        print (self.sid, '<<<',)
        
        try:
            rec = self.s.recv(1024)
        except socket.error:
            self.hold_state('Stopped connection')
            
        print (rec)


        if len(rec) > 3:
            
            if rec[3] == '-':
                return rec+self.recv()
        return rec        

    def send(self, mes='', CRLF=True, filt=''):
        print (self.sid, '>>>',)

        try:
            self.s.send(mes + ('', '\r\n')[CRLF==True])

        except socket.error:
            self.hold_state('Connection reset')

        if CRLF:
            if filt:
                print (mes.replace(filt, '*'*len(filt)))
            else:
                print (mes)

class ftp_client:
	
    def __init__(self):

        self.timezone = 0
        self.buffer_size = 1024
        self.sock_pasv = False
      
    def connect(self):
        self.sock.connect(())
        
    def send(self,msg):
        totalsent = 0
        MSGLEN=len(msg)
        while totalsent < MSGLEN:
            sent = self.sock.send(msg[totalsent:])
            if sent == 0:
                raise RuntimeError, "socket connection broken"
            totalsent = totalsent + sent
            
    def sendcmd(self,cmd):
        cmd = cmd + "\r\n"
        self.send(cmd)
	
    def LOGIN(self, usern, passw):
        self.sock_main.relay('USER '+usern)
        res = self.sock_main.relay('PASS '+passw, filt=passw)

        if self.handle.get_id(res) != 230:
            self.error(UNEXPECTED_RESPONSE, 'incorrect username or password')
		
    def DIR(self):

        self.PASV()
        msg = self.sock_main.relay('NLST')
        
        if self.handle.validify_case(msg):

            msg = ''
            add = True
            while add != '':
                add = self.sock_pasv.recv()
                msg += add
            self.think('Empty message sent. File list is done.')
            self.sock_pasv.cls()
        
            flist = self.handle.parse_nlst(msg)
            self.think(flist)
        
           
            self.sock_main.recv(226)

        else:
            self.sock_pasv.cls()
            flist = []
        
        return flist
        
     def CDUP(self):
        self.sock_main.relay('CDUP')

    def MODE(self, m='S'):
        self.sock_main.relay('MODE '+m)

    def TYPE(self, t='A'):
        self.sock_main.relay('TYPE '+t)
        
    def CWD(self, dname):
        self.sock_main.relay('CWD '+dname, 250)
        
    def MKD(self, dname):
        self.sock_main.relay('MKD '+dname, 257)
        
    def PASV(self):
        

        if self.sock_pasv:
            self.think('Checking for open socket')
            assert not self.sock_pasv.open 
        
        msg = self.sock_main.relay('PASV')
        newip, newport = self.handle.parse_pasv(msg)

        self.sock_pasv = mk_socket(2, newip, newport)

        return newip, newport 

       
	
        
#-----------------------------------------------------------------
    MYclient = ftp_client()
    
    try:
        MYclient.connect()
        
    except socket.error as error:
        print ("Could not connect")
        sys.exit(1)
        
    try:
        MYclient.LOGIN(input("userftp"), input("r3d3sf1s1c@s"))
        
    except UNEXPECTED_RESPONSE:
        print ("Incorrect login")
        sys.exit(1)
    

    MYclient.QUIT()

