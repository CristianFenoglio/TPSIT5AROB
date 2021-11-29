import socket
import threading as thr
import time

server=("localhost", 12001) #indirizzo e porta del server

class Receiver(thr.Thread):
    '''
    classe thread che permette di ricevere i messaggi dal server 
    e rispondere con la soluzione del calcolo
    '''
    def __init__(self, s):
        thr.Thread.__init__(self)
        self.running = True
        self.s = s

    def stop_run(self):
        self.running = False

    def run(self):
        while self.running:
            operation = self.s.recv(4096).decode()
            print(operation)
            if operation == "exit":
                self.stop_run()
            else:
                answer = eval(operation)
                self.s.sendall(str(answer).encode())

def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(server)

    ricev = Receiver(s)
    ricev.start()

    while True:
        '''
         while che si interrompe appena l'oggetto 
         della classe Receiver finisce il suo operato
        '''
        time.sleep(0.2)
        if ricev.running == False:#chiusura del thread
            ricev.join()
            s.close()
            break

if __name__ == "__main__":
    main()