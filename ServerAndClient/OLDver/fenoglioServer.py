'''
messaggi = 
richiesta+ , + nome [+ , +  par1]

'''


import threading as thr
import time
import socket as sck
import sqlite3

CLIENT=('localhost',6004)
DictCor = {}
threads = []


def create_connection(db_file):
    '''
    crea una connesione dato il path di un database
    '''
    conn = None
    conn = sqlite3.connect(db_file)
    
    return conn


def numeroMaxClient():#trovo il numero di client
    db = create_connection("./file.db")
    return contatore(db)

def contatore(conn):
    cur = conn.cursor()
    cur.execute(f"SELECT max(id_frammento) FROM frammenti")
    rows = cur.fetchall()
    for row in rows:
        return row[-1]





'''
le 4 funzioni per calcolare la risposta delle interrogazioni
'''
def findtheFile(conn, nomFile):#trovas il file
    lstNom=[]
    cur = conn.cursor()
    cur.execute(f"SELECT nome FROM files")
    rows = cur.fetchall()
    for row in rows:
        lstNom.append(row[-1])
    return nomFile in lstNom



def numfram(nomFile):#trova il numero di thread con il file richiesto (i frammenti senza thread non sono contati)
    count=0
    print(threads)
    for c in threads:
        if c.getnome == nomFile:
            count+=1
    return count 

def whohavefragment(nomFile, framment):#indirizzo di chi has il frammanto
    for c in threads:
        if c.getnome()==nomFile and c.getframment()==framment:
            return c.getind()
    return 
def whohavefile(nomFile):#indirizzo di tutti quelli che hanno il frammento di quel film
    toret=[]
    for c in threads:
        if c.getnome()==nomFile:
            toret.append(c.getind())
    return toret

global nMaxClient
nMaxClient = numeroMaxClient()

class Client_Class(thr.Thread):
    def __init__(self, connection, addr, num_client, db):#numclient corrisponde all id frammento
        thr.Thread.__init__(self)
        self.addr = addr
        self.connection = connection
        self.running = True
        self.num_client = num_client
        self.db=db

        '''
        carticamento dei "dati personali" del thread, ovvero nome, indirizzo e numero frammento
        '''
        conn=create_connection(db)
        cur = conn.cursor()
        cur.execute(f"SELECT files.nome FROM files, frammenti where frammenti.id_file = files.id_file and frammenti.id_frammento=={num_client}")
        rows = cur.fetchall()
        self.nome=rows[0][-1]
        cur.execute(f"SELECT n_frammento from frammenti where frammenti.id_frammento=={num_client}")
        rows = cur.fetchall()
        self.framment=rows[0][-1]
        cur.execute(f"SELECT host from frammenti where frammenti.id_frammento=={num_client}")
        rows = cur.fetchall()
        self.ind=rows[0][-1]
        conn.close()



    def getnome(self):
        return self.nome
    def getframment(self):
        return self.framment
    def getind(self):
        return self.ind

    
    def stop_run(self):
        self.running = False

    def ret_run(self):
        return self.running
    
    def run(self):
        while self.running:
            questionpar=self.connection.recv(4096).decode()
            print("arrivato mess   "+ questionpar)
            if questionpar=="exit":
                self.stop_run()
                break
            questionpar=questionpar.split(",")
            '''
            il messaggio come scritto sopra contiene la richiesta della funzione + , + vari parametri
            '''

            question=questionpar[0]
            print("funzione richiesta :   "+question)

            print("miei dati")
            print(self.nome)
            print(self.framment)
            print(self.ind)
            '''
            trova la funzione
            '''
            if question=="find":
                answ=findtheFile(create_connection(self.db), questionpar[1])
            
            elif question== "num":
                answ=numfram(questionpar[1])
            elif question=="who fragm":
                answ=whohavefragment(questionpar[1], questionpar[2])
            elif question=="who file":
                answ=whohavefile(question[1])
                
            else:
                answ="funzione non trovata"
            self.connection.sendall(str(answ).encode())
            print(answ)
            
                
            
class Thread_remover(thr.Thread):
    '''
    classe che rimuove i thread allas loro chiusura
    '''
    def __init__(self):
        thr.Thread.__init__(self)
        self.running = True

    def run(self):
        while self.running:
            for i in threads:
                if not i.ret_run():
                    i.join()
                    threads.remove(i)
            

def main():
    global nMaxClient

    s = sck.socket(sck.AF_INET, sck.SOCK_STREAM)
    s.bind(CLIENT)
    s.listen()

    thread_stopper = Thread_remover()
    thread_stopper.start()

    client_counter = 0

    while True:
        '''
        crea i variu thread all arrivo di un nuovo client
        '''
        connection, addr = s.accept()
        client_counter += 1
    
        client = Client_Class(connection, addr, client_counter, "./file.db")

        threads.append(client)
        client.start()
        time.sleep(0.2)

        #print(client_counter)
        if client_counter >= nMaxClient:#se si supera il numero max il programma si chiude
            break
        

    for k in threads:
        k.stop_run()

    s.close()

if __name__ == "__main__":
    main()