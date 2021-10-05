import socket as sck
import threading as thr
import time
LOCAL = ('localhost', 5000)
SERVER = ('192.168.0.126', 5000)
registred=False
nameself=""
frasetosstamp=""


class ricevitore(thr.Thread):
    def __init__(self, socket):
        thr.Thread.__init__(self)#(super in java)
        self.socket=socket
        self.running=True
    def stopRun(self):
        self.running=False
    
    def run(self):
        global registred
        while self.running:
            msg_received= self.socket.recv(4096)
            if msg_received=="ok":
                registred=True
                print("registrato")
            else:
                print(f"\n{msg_received}")
                print(f"\n{frasetosstamp}")

def main():
    s = sck.socket(sck.AF_INET, sck.SOCK_STREAM)
    s.connect(SERVER)
    print("Connessione avvenuta")
    reciv=ricevitore(s)
    reciv.start()
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
       
        s.sendall(msg.encode())
        
        if  "exit" in msg.split(":"):
            print(f"Disconnessione...")
            break
    reciv.stopRun()
    reciv.join()
    s.close()

if __name__ == "__main__":
    main()