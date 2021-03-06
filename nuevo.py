#!/user/bin/python3

import sys, socket, re, os, string, time, glob, curses, curses.textpad
from os import system


class mk_socket:
    
    def __init__(self, host, port=21):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((host, port))
        self.open = True
        
    def enviar(self, mes=""):
        aux = bytes(mes+'\r\n').encode('utf-8')
        print (aux)
        self.s.send( aux )
        return self.recibir()
    
    def enviar_cacho(self, mes="", tipo = 'A'):
        aux = ''
        if tipo == 'A':
            aux = bytes(mes).encode('utf-8')
        else:
            aux = mes
        self.s.send( aux )
    
    def recibir(self):
        rec = self.s.recv(1024)
        return rec
        
    def cerrar(self):
        if self.open:
            self.s.close()
            self.open = False

        
            
class Archivo:

    def __init__(self, nombre):
        self.f = open(nombre, 'r')
        self.tamano = os.stat(nombre)[6]
        self.pos = 0
        self.open = True

    def next(self, buff=1024):

        self.f.seek(self.pos)
        self.pos += buff

        if self.pos >= self.tamano:
            buf = self.f.read(-1)
            self.f.close()
            self.open = False
        else:
            buf = self.f.read(buff)
            
        return buf
            
            
        
class ftp_client:
    def __init__(self):
        self.timezone = 0
        self.buffer_size = 1024
        self.puerto_pasivob = False
        self.tipo = 'A'
        self.puerto_pasivo = False
        
    def connectar(self, host, port=21):
        self.sock_main = mk_socket(host, port)

    def LOGIN(self, usern, passw):
        us = self.sock_main.enviar('USER '+usern)
        print (us)
        passw = self.sock_main.enviar('PASS '+passw)
        print (passw)
        time.sleep(0.5)
        print (self.sock_main.recibir())
        
    def lista(self):
        if self.puerto_pasivob == 0:
            self.pasivo()
        
        self.sock_main.enviar('LIST')
        msg = ''
        add = True
        while add != '':
            add = self.puerto_pasivo.recibir()
            msg +=  add
        aux = msg.split('\r\n')
        listar = ''
        for i in range(len(aux)):
            aux2 = aux[i].split(' ')
            dir = aux2[0]
            ar = aux2[len(aux2) - 1]
            listar += ('/', '')[dir.find("d")] + ar + '\r\n'
        print(listar)
        self.puerto_pasivob = True
        return listar
            
    def Borrar(self, cosa):
        self.sock_main.enviar('DELE '+cosa)
    
    def CDD(self, directorio):
        self.sock_main.enviar('CWD '+directorio)
        
    def CND(self, directorio):
        self.sock_main.enviar('MKD '+directorio)
        
    def pasivo(self):
        time.sleep(1)
        
        res = self.sock_main.enviar('PASV')
        print (res)
        n_res = res.split('(')[-1].split(')')[0]
        p = n_res.split(',')
        ip, puerto = '.'.join(p[:4]), int(p[4])*256 + int(p[5])
        self.puerto_pasivo = mk_socket(ip, puerto)
    
    def subir(self, fname, fsource):
        if self.puerto_pasivob == 0:
            self.pasivo()
        
        self.sock_main.enviar('STOR '+fname)
        nuevo = Archivo(fsource)
        print (5)
        while nuevo.open == True:
            self.puerto_pasivo.enviar_cacho(nuevo.next(self.buffer_size), self.tipo) 
            print (5)
        self.puerto_pasivo.cerrar()
        time.sleep(0.5)
        print (self.sock_main.recibir())
        #self.puerto_pasivob = True

    def Permisos(self, modo='555', arc=''):
        self.sock_main.enviar('SITE CHMOD '+modo+' '+arc)
    
    def TYPE(self, t='A'):
        self.sock_main.enviar('TYPE '+t)
        self.tipo = t
        
    def bajar(self, fname, fsource):
        if self.puerto_pasivob == 0:
            self.pasivo()
        self.sock_main.enviar('RETR '+fname)
        msg = ''
        add = True
        while add != '':
            add = self.puerto_pasivo.recibir()
            msg += add
        file = open(fsource,'w')
        file.write(msg)
        #self.puerto_pasivob = True
        
    def Mostrar_dirLoc(self, dir = "/"):
        stri = '\r\n'.join(os.listdir(dir))
        return stri


def get_param(prompt_string):
     screen.clear()
     screen.border(0)
     screen.addstr(2, 2, prompt_string)
     screen.refresh()
     input = screen.getstr(10, 10, 60)
     return input
     
def imp(mens):
    screen.clear()
    screen.addstr(2,2, mens)
    screen.getstr(1, 1, 60)
def impl(listar):
    screen.clear()
    screen.border(0)
    aux = listar.split("\r\n")
    for i in range(len(aux)):
        screen.addstr(int(i+2), 2, str(aux[i]))
    screen.getstr(1, 1, 60)
    
if __name__ == '__main__':
    
    #stdscr = curses.initscr()
    #while 1:
    #    c = stdscr.getch()
    #    if c == ord('p'):
    #        PrintDocument()
    #    elif c == ord('q'):
    #        break  # Exit the while()
    #    elif c == curses.KEY_HOME:
    #        x = y = 0
    #curses.endwin()
    
    #res = '(12,12,12,12,12,250)'
    #n_res = res.split('(')[-1].split(')')[0]
    #p = n_res.split(',')
    #ip, port = '.'.join(p[:4]), int(p[4])*256 + int(p[5])
    #print (ip)
    #print (port)
    MYclient = ftp_client()
    print (MYclient.Mostrar_dirLoc("/home/ec2-user/"))
    x = 0
    bc = False
    bu = False
    fint = False
    if raw_input('Quieres ver la beta de ncurses? (y/n)') == 'y':
        while x != ord('4'):
            screen = curses.initscr()

            screen.clear()
            screen.border(0)
            screen.addstr(2, 2, "Please enter a number...")
            screen.addstr(4, 4, "1 - Seleccionar servidor")
            screen.addstr(5, 4, "2 - Seleccionar Usuario")
            screen.addstr(6, 4, "3 - Navegar directorio local")
            screen.addstr(7, 4, "4 - Enviar Archivo")
            screen.addstr(8, 4, "5 - Ver directorio remoto")
            screen.addstr(9, 4, "6 - Bajar archvo")
            screen.addstr(10, 4, "7 - Cambair directorio de trabajo")
            screen.addstr(11, 4, "8 - Cambiar permisos de archivos")
            screen.addstr(12, 4, "9 - Borrar archivos")
            screen.addstr(13, 4, "a - Cambiar carpeta remota")
            screen.addstr(14, 4, "b - Crear carpeta remota")
            screen.addstr(15, 4, "c - Cambiar modo (ascii o bin)")
            screen.addstr(16, 4, "d - Cambiar permisos a archivos")
            screen.addstr(17, 4, "e - Exit")
            screen.refresh()

            x = screen.getch()
            
            
            if x == ord('1'):
                if bc:
                    imp('Ya te conectaste')
                else:
                    username = get_param("direccion IP del servidor")
                    puert = get_param("puerto del servidor")
                    MYclient.connectar(username, int(puert))
                    bc = True
                    curses.endwin()
                
            
            if x == ord('2'):
                if bc:
                    if bu:
                        imp('Ya te logeaste')
                    else:
                        username = get_param("usuario")
                        cont = get_param("contrasena")
                        MYclient.LOGIN(username, cont)
                        bu = True
                        curses.endwin()
                else:
                    imp('\r\nDebes de conectarte a un servidor primero')

            if x == ord('3'):
                direct = get_param("Dame un directorio valido desde la raiz (ruta absoluta)") 
                impl(MYclient.Mostrar_dirLoc(direct))
                curses.endwin()
            
            if x == ord('8'):
                if (bc==True) and (bu==True):
                    imp("exito")
                    curses.endwin()
                else:
                    imp("Conectate primero a un servidor con un usuario valido")                    
                    
            if x == ord('4'):
                if (bc==True) and (bu==True):
                    archi = get_param("Dame el archivo (con su ruta oabsoluta)")
                    nom = get_param("Dame el nombre con el que se va a mostrar el archivo")
                    MYclient.subir(nom, archi)
                    curses.endwin()
                else:
                    imp("Conectate primero a un servidor con un usuario valido")                    

            if x == ord('5'):
                if (bc==True) and (bu==True):
                    archi = MYclient.lista()
                    impl(archi)
                    curses.endwin()
                else:
                    imp("Conectate primero a un servidor con un usuario valido")
                    
            if x == ord('7'):
                if (bc==True) and (bu==True):
                    archi = get_param("Dame la ruta con el nombre incorporado (del archivo a crear/escribir)")
                    nom = get_param("Dame el nombre del archivo en el servidor")
                    MYclient.subir(nom, archi)
                    curses.endwin()
                else:
                    imp("Conectate primero a un servidor con un usuario valido")

            if x == ord('9'):
                if (bc==True) and (bu==True):
                    nom = get_param("Dame el nombre del archivo ea eliminar")
                    MYclient.Borrar(nom)
                    curses.endwin()
                else:
                    imp("Conectate primero a un servidor con un usuario valido")                    
            
            if x == ord('a'):
                if (bc==True) and (bu==True):
                    nom = get_param("Dame el nombre del directorio")
                    MYclient.CDD(nom)
                    curses.endwin()
                else:
                    imp("Conectate primero a un servidor con un usuario valido")
            
            if x == ord('b'):
                if (bc==True) and (bu==True):
                    nom = get_param("Dame el nombre del directorio a crear")
                    MYclient.CND(nom)
                    curses.endwin()
                else:
                    imp("Conectate primero a un servidor con un usuario valido")
            
            if x == ord('c'):
                if (bc==True) and (bu==True):
                    nom = get_param("Dame a cual quieres cambiarlo, A - ascii o I - Bin")
                    MYclient.TYPE(nom)
                    curses.endwin()
                else:
                    imp("Conectate primero a un servidor con un usuario valido")
            
            if x == ord('d'):
                if (bc==True) and (bu==True):
                    archi = get_param("Dame el nombre del archivo a cambiar permisos")
                    nom = get_param("El tipo de permisos que le vas a asignar (ej. 755)")
                    MYclient.Permisos(nom, archi)
                    curses.endwin()
                else:
                    imp("Conectate primero a un servidor con un usuario valido")
            
            if x == ord('e'):
                break
        curses.endwin()
        
    else:    
        #MYclient.Mostrar_dirLoc("/")
        MYclient.connectar(raw_input('Direccion: '), int(raw_input('Puerto: ')))
        MYclient.LOGIN(raw_input('Usuario: '), raw_input('Contrasena: '))

    
        variable = raw_input('Que quieres probar, binario o ascii (b/a)')
    
        if variable == 'b':
            MYclient.TYPE('I')
            MYclient.bajar('pokebola.png', '/home/ec2-user/pokebola.png')
            MYclient.subir('pokebola5.png', '/home/ec2-user/pokebola.png')
            MYclient.TYPE()
            MYclient.lista()
        elif variable == 'a':
            MYclient.bajar('p131.py', '/home/ec2-user/p131.py')
            MYclient.subir('p48.py', '/home/ec2-user/p131.py')
            MYclient.lista()
        else:
            print ("opcion no valida, adios")
        MYclient.Mostrar_dirLoc('/home/ec2-user/')
    #MYclient.CDD('Tecu')
    
    #MYclient.TYPE('I')
    
    #MYclient.lista()
    
    #MYclient.bajar('p131.py', '/home/ec2-user/p131.py')
    
    
    #MYclient.TYPE('I')
    
    #MYclient.bajar('pokebola.png', '/home/ec2-user/pokeball.png')
    
    #MYclient.CDD('Tecu')
            
    #MYclient.subir('p133.py', '/home/ec2-user/p131.py')
    
    
    
    #MYclient.lista()
    #MYclient.CND('Tecu')
    
