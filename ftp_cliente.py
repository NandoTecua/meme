import sys, socket, re, os, string, time, urllib2
class mysocket:
    '''Socket stolen somewhere from the net'''
    def __init__(self, sock=None):
        if sock is None:
            self.sock = socket.socket(
                socket.AF_INET, socket.SOCK_STREAM)
        else:
            self.sock = sock
    def connect(self,host, port):
        self.sock.connect((host, port))
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
		
	 def QUIT(self):
        if self.sock_pasv:
            if self.sock_pasv.open:
                self.think('Passive port open... closing')
                self.sock_pasv.cls()
            else:
                self.think('Passive port already closed')
        self.sock_main.relay('QUIT')
        self.sock_main.cls()
		
	def get_file(s, file_name):
		cmd = 'get\n%s\n' % (file_name)
		s.sendall(cmd)
		r = s.recv(2)
		size = int(s.recv(16))
		recvd = ''
		while size > len(recvd):
			data = s.recv(1024)
			if not data: 
				break
			recvd += data
		s.sendall('ok')
		return recvd
		
    def getResult(self):
        result=""
        line=""
        while line[0:3] != "end":
            line=self.getline()
            if line[0:3] != "end":
                result=result+line
        return result
    def receive(self):
        msg = ''
        while len(msg) < MSGLEN:
            chunk = self.sock.recv(MSGLEN-len(msg))
            if chunk == '':
                raise RuntimeError, "socket connection broken"
            msg = msg + chunk
        return msg
		
	def recvfile(s, filename):
    
		cmds = filename.split(" ")
		fname = " ".join(cmds[1:])
		
		 FILE = open(fname, "w+")
		FILE.close()
		s.send("_BEGIN_")
		print "Downloading file: " + fname
		rf = open(fname,'wb')
		while True:
		   data = s.recv(1024)
		   if(len(data)<= 0):
			 break
		   rf.write(data)
		rf.close()
		print "Finished Dowloading file:  " + fname
		
    def getline(self):
        msg=''
        chunk='a'
        while chunk != '\n':
            chunk=self.sock.recv(1)
            if chunk == '':
                raise RuntimeError, "socket connection broken"
            if chunk != '\n':
                msg=msg+chunk
        return msg
#-----------------------------------------------------------------
s=mysocket()
try:

    if len(sys.argv) != 4:
       
    else:
        ql=open(sys.argv[1],"r")
        host=sys.argv[2]
        port=int(sys.argv[3])
        try:
            s.connect(host,port)
        except:
            print "Connecting to server "+host+" on port "+str(port)+" failed."
            
            
        files=ql.readlines()
        ql.close()
        s.sendcmd("setresults 10")
        s.sendcmd("setextensions 2")
    
        for file in files:
            file=re.sub('\n','',file)
            cmd="retrieveandsaveranks 1030 "+file+".ranks "+file
            s.sendcmd(cmd)
            res=s.getline()
            print res
            
        s.sendcmd("bye")
            
except Exception, e:
    s.sendcmd("bye")
    print e

    time.sleep(1)
