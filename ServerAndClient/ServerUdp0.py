'''
costruire una chat, che affronti il problema "come fa alice a scrivere a bob?
UDP
bisogna identificare unicamente ogni utente

----------
| server |      
----------
|nick| ip| (dizionario)

se un client si collega: manda un messaggio al server(così si ottiene l'ip)
quando riceve l'"hello" il server risponde con l'"ok"

"hello"=f"NICKNAME: {nick_name}"
"ok"="ok"



messaggi x parlarsi= f"{nickMITTENTE}: {nickDESTINAZIONE}:{messaggio}"


farlo in TCP
creare il comando !LIST-->manda la lista degi utenti f"LIST:{dict.keys()}
'''
import socket as sck
from sys import addaudithook

LOCAL = ('localhost', 5000)
SERVER = ('0.0.0.0', 5000)
OK="ok"
class NickTable():
    def __init__(self, sck):
        self.table={}
        self.s=sck
        self.cnt=0
    def doyourjob(self):
        hello, addr=self.s.recvfrom(4096)
        hello=hello.decode()
        if "NICKNAME" == str(hello).split(":")[0].upper():
            try:
                name= hello.split(":")[1]
            except Exception:
                name=f"guest{self.cnt}"
                self.cnt+=1
            
            self.table[name]=addr
            self.s.sendto(OK.encode(), addr)
            print(f'nuovo utente aggiunto :{name} {self.table[name]}')
            print(self.table)
        else:
            msg=hello.split(":")
            invier=msg[0]
            forWho=msg[1]
            whatMsg=msg[2]
            if forWho not in self.table:
                self.s.sendto("utente non trovato".encode(), addr)
            else:
                self.s.sendto(f"{invier}:: {whatMsg}".encode(), self.table[forWho])
                print(f' {invier} scrive a {forWho} : {whatMsg}')



        
        
            
        
        

def main():
    s = sck.socket(sck.AF_INET, sck.SOCK_DGRAM)
    s.bind(('0.0.0.0', 5000))
    users=NickTable(s)
    while True:
        users.doyourjob()
        
    s.close()

if __name__ == "__main__":
    main()