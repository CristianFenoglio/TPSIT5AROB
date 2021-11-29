import socket
import threading as thr
import time


class Receiver(thr.Thread):
    def __init__(self, s): 
        thr.Thread.__init__(self)
        self.running = True 
        self.s = s

    def stop_run(self):
        self.running = False

    def run(self):

        while self.running:
            data = self.s.recv(4096).decode()

            print(f"\n{data}")

def main():
    global registered
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('localhost', 5000))

    client = Receiver(s)
    client.start()

    while True:
        time.sleep(0.2)

        way = input("Insert the direction (forward, backward, right, left, stop) >>>")

        s.sendall(way.encode())

        if 'exit' in way.split(":"):
            client.stop_run()
            print("Disconnection...")
            break

    client.join()
    s.close()

if __name__ == "__main__":
    main()