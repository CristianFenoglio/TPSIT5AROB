'''

messaggi x parlarsi= f"{nickMITTENTE}: {nickDESTINAZIONE}:{messaggio}"
'''


import socket as sck
import threading as thr
import time

LOCAL = ('localhost', 5000)
SERVER = ('192.168.0.126', 5000)
registred=False
nameself=""
frasetosstamp=""
class ricevitore(thr.Thread):
    def __init__(self, port, s):
        thr.Thread.__init__(self)
        self.port = port#porta
        self.s = s#soket
        self.running = True
    def run(self):
        global registred
        while self.running:
            data,_ = self.s.recvfrom(self.port)
            msg_received = data.decode()
            if msg_received=="ok":
                registred=True
                print("registrato")
            else:
                print(f"\n{msg_received}")
                print(f"\n{frasetosstamp}")

def main():
    global registred
    global nameself
    s = sck.socket(sck.AF_INET, sck.SOCK_DGRAM)
    rec = ricevitore(SERVER[1], s)
    rec.start()
    global frasetosstamp
    while True:
        time.sleep(0.2)
        if not registred:
            
            mess=input("inserisci il tuo nome  ")
            nameself=mess
            msg="NICKNAME:"+mess
            registred=True
            
        else:
            frasetosstamp="inserisci il destinatario  "
            dst=input("inserisci il destinatario  ")
            frasetosstamp="inserisci il testo  "
            mess=input("inserisci il testo  ")
            frasetosstamp="inserisci il destinatario  "
            msg=nameself+":"+dst+":"+mess
       
        
        s.sendto(msg.encode(), SERVER)
        
        


if __name__ == '__main__':
    main()
