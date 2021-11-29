import threading as thr
import os
import time
import socket as sck
import sqlite3

CLIENT=('localhost',12001)#porta 120001
lista_client = {}
threads = []

def create_connection(db_file):
    '''
    crea una connessione con il file del database
    '''
    conn = sqlite3.connect(db_file)
    return conn

def operation_selecter(conn, client_num):
    '''
    data la connessione col database e il numero identificativo del client fa
    una ricerca su quell identificativo
    '''
    list = []
    cur = conn.cursor()
    cur.execute(f"SELECT operation FROM operations Where client = {client_num}")

    rows = cur.fetchall()

    for row in rows:
        list.append((row[-1]))

    return list

def contatore(conn):
    '''
    data la connesssione trova il massimo numero del client nell'database
    '''
    cur = conn.cursor()
    cur.execute(f"SELECT max(client) FROM operations")

    rows = cur.fetchall()

    for row in rows:
        return row[-1]


def numeroMaxClient():
    '''
    restituisce dal database operations.db il numero massimo di client possibili
    '''
    db = create_connection("./operations.db")
    return contatore(db)
    db.close()

global nMaxClient#numero massimo di client possibili, visto che è quel numero massimo nel database
nMaxClient = numeroMaxClient()

class Client_Class(thr.Thread):
    '''
    la classe Thread per la gestione dei client
    '''
    def __init__(self, connection, addr, num_client):
        thr.Thread.__init__(self)
        self.addr = addr
        self.connection = connection
        self.running = True
        self.num_client = num_client

    def stop_run(self):
        self.running = False

    def ret_run(self):
        return self.running
    
    def run(self):
        while self.running:
            '''
            crea la connessione col database
            estrae le operazioni necessarie al client
            invia le operazioni dal client e poi aspetta la risposta con il risultato
            printa il risultato
            '''
            db = create_connection("./operations.db")
            operation_list = operation_selecter(db, self.num_client)
            db.close()
            for element in operation_list:
                self.connection.sendall(element.encode())
                answ = self.connection.recv(4096).decode()
                print(f"client: {self.num_client} answered: {element} --> answer: {answ}")
            self.connection.sendall("exit".encode())
            self.stop_run()
            


class Thread_remover(thr.Thread):
    '''
    classe thread che rimuove i client thread
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
    '''
    inizializzazione server
    crea l'oggetto della classe thread_remover per poter eliminare, a tempo debito, 
    i thread che in futuro si fermeranno 
    '''
    global nMaxClient

    s = sck.socket(sck.AF_INET, sck.SOCK_STREAM)
    s.bind(CLIENT)
    s.listen()
    
    thread_stopper = Thread_remover()
    thread_stopper.start()

    client_counter = 0# conta il numero di client presenti per controllare la presenza di troppi client e assegnare ad ognun glient un "numero identificativo"

    while True:
        '''
        aspetta una connessione e quando un client si connette, aumenta il numero di client, crea un oggetto 
        della classe client e fa il controllo sul numero di client
        '''
        connection, addr = s.accept()
        client_counter += 1
    
        client = Client_Class(connection, addr, client_counter)

        threads.append(client)#aggiunge alla lista dei thread il nuovo thread
        client.start()
        time.sleep(0.2)


        if client_counter > nMaxClient:# in caso si superi il numero di client massimo il programma trermina
            break
        
    '''chiusura'''
    for k in threads:
        k.stop_run()

    s.close()

if __name__ == "__main__":
    main()