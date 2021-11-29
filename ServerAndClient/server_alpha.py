import socket as sck
from sqlite3.dbapi2 import SQLITE_DELETE
import threading as thr
import time
import RPi.GPIO as GPIO
import time as T
import sqlite3 as SQL
import subprocess as sb

class AlphaBot(object):
    
    def __init__(self, in1=13, in2=12, ena=6, in3=21, in4=20, enb=26):
        self.IN1 = in1
        self.IN2 = in2
        self.IN3 = in3
        self.IN4 = in4
        self.ENA = ena
        self.ENB = enb
        self.PA  = 41  #left engine
        self.PB  = 38  #right engine

        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self.IN1, GPIO.OUT)
        GPIO.setup(self.IN2, GPIO.OUT)
        GPIO.setup(self.IN3, GPIO.OUT)
        GPIO.setup(self.IN4, GPIO.OUT)
        GPIO.setup(self.ENA, GPIO.OUT)
        GPIO.setup(self.ENB, GPIO.OUT)
        self.PWMA = GPIO.PWM(self.ENA,500)
        self.PWMB = GPIO.PWM(self.ENB,500)
        self.PWMA.start(self.PA)
        self.PWMB.start(self.PB)
        self.stop()

    def forward(self, time_ms):  #this function moves the alphabot forward for {time_ms} milliseconds
        print("The Alphabot moves forward...")
        

        self.PWMA.ChangeDutyCycle(self.PA)      #setting the engines
        self.PWMB.ChangeDutyCycle(self.PB)
        GPIO.output(self.IN1, GPIO.LOW)
        GPIO.output(self.IN2, GPIO.HIGH)
        GPIO.output(self.IN3, GPIO.HIGH)
        GPIO.output(self.IN4, GPIO.LOW)

        T.sleep(time_ms/1000)
        self.stop()


    def backward(self, time_ms):        #this function moves the alphabot backward for {time_ms} milliseconds
        print("The Alphabot moves backward...")

        self.PWMA.ChangeDutyCycle(self.PA)      #setting engines
        self.PWMB.ChangeDutyCycle(self.PB)
        GPIO.output(self.IN1, GPIO.HIGH)
        GPIO.output(self.IN2, GPIO.LOW)
        GPIO.output(self.IN3, GPIO.LOW)
        GPIO.output(self.IN4, GPIO.HIGH)

        T.sleep(time_ms/1000)
        self.stop()

    def left(self, time_ms):        #this function turns left the alphabot for {time_ms} milliseconds
        print("The Alphabot moves left...")
        
        self.PWMA.ChangeDutyCycle(self.PA)      #setting the engines
        self.PWMB.ChangeDutyCycle(self.PB)
        GPIO.output(self.IN1, GPIO.HIGH)
        GPIO.output(self.IN2, GPIO.LOW)
        GPIO.output(self.IN3, GPIO.HIGH)
        GPIO.output(self.IN4, GPIO.LOW)

        T.sleep(time_ms/1000)
        self.stop()

    def right(self, time_ms):       #this function turns right the alphabot for {time_ms} milliseconds
        print("The Alphabot moves right...")
        
        self.PWMA.ChangeDutyCycle(self.PA)      #setting the engines
        self.PWMB.ChangeDutyCycle(self.PB)
        GPIO.output(self.IN1, GPIO.LOW)
        GPIO.output(self.IN2, GPIO.HIGH)
        GPIO.output(self.IN3, GPIO.LOW)
        GPIO.output(self.IN4, GPIO.HIGH)

        T.sleep(time_ms/1000)
        self.stop()

    def stop(self, time_ms = 0):        #this function stops the alphabot for {time_ms} milliseconds
        print("The Alphabot stops...")

        self.PWMA.ChangeDutyCycle(0)
        self.PWMB.ChangeDutyCycle(0)
        GPIO.output(self.IN1, GPIO.LOW)
        GPIO.output(self.IN2, GPIO.LOW)
        GPIO.output(self.IN3, GPIO.LOW)
        GPIO.output(self.IN4, GPIO.LOW)

        T.sleep(time_ms/1000)
        
    def set_pwm_a(self, value):
        self.PA = value
        self.PWMA.ChangeDutyCycle(self.PA)

    def set_pwm_b(self, value):
        self.PB = value
        self.PWMB.ChangeDutyCycle(self.PB)    
        
    def set_motor(self, left, right):       #this function sets engines
        if (right >= 0) and (right <= 100):
            GPIO.output(self.IN1, GPIO.HIGH)
            GPIO.output(self.IN2, GPIO.LOW)
            self.PWMA.ChangeDutyCycle(right)
        elif (right < 0) and (right >= -100):
            GPIO.output(self.IN1, GPIO.LOW)
            GPIO.output(self.IN2, GPIO.HIGH)
            self.PWMA.ChangeDutyCycle(0 - right)
        if (left >= 0) and (left <= 100):
            GPIO.output(self.IN3, GPIO.HIGH)
            GPIO.output(self.IN4, GPIO.LOW)
            self.PWMB.ChangeDutyCycle(left)
        elif (left < 0) and (left >= -100):
            GPIO.output(self.IN3, GPIO.LOW)
            GPIO.output(self.IN4, GPIO.HIGH)
            self.PWMB.ChangeDutyCycle(0 - left)

alphabot = AlphaBot()       #this is the object of the class Alphabot()

class Clients_class(thr.Thread):        #class client
    global alphabot

    def __init__(self, connessione, addr):
        thr.Thread.__init__(self)
        self.addr = addr
        self.connessione = connessione
        self.running = True

    def stop_run(self):
        self.running = False

    def ret_run(self):
        return self.running
    def basicMovements(self, way, time=1000):       #understand if the command given is a basic movement or not and does it
        if 'exit' in way:
            self.running = False
            self.connessione.close()
            alphabot.stop()
            print("Disconnection...")
        
        #recognise the letter (w-a-s-d) for the direction
        elif 'w' in way:        #forward
            self.connessione.sendall("OK".encode())
            alphabot.forward(time)
        
        elif 's' in way:        #backward
            self.connessione.sendall("OK".encode())
            alphabot.backward(time)
        
        elif 'a' in way:    #left
            self.connessione.sendall("OK".encode())
            alphabot.left(time)

        elif 'd' in way:    #right
            self.connessione.sendall("OK".encode())
            alphabot.right(time)

        elif 'e' in way:    #stop
            self.connessione.sendall("OK".encode())
            alphabot.stop(time)

    def run(self):
        while self.running:
            way = (self.connessione.recv(4096)).decode()        #recieve the command
            if way == "battery":                                #battery level control
                self.connessione.sendall(control())

            if ":" in way and way.split(":")[0] in ["exit", "w", "s", "a", "d", "e"]:     #recognise if the command is a basic movement
                time = int(way.split(":")[1])   #splitting the command in move and time
                way = way.split(":")[0]
                self.basicMovements(way, time)
            

            else:       #if is not a basic movement, we search it in our database
                connessione_db = SQL.connect('./alphabot.db')
                cursor = connessione_db.cursor()        #creating the cursor
                cursor.execute(f"SELECT Movimenti.sequenza FROM Movimenti WHERE '{way}' = Movimenti.nome")      #searching the sequence of moves in the DB
                temporan = cursor.fetchall()    #execute the query
                if len (temporan)>0:
                    movimenti=temporan[0][0]
                    for m in movimenti.split(","):
                        self.basicMovements(m.split(":")[0], int(m.split(":")[1]))
                    connessione_db.close()

def control():
    out = sb.check_output(["vcgencmd", "get_throttled"])    #battery control with library subprocess
    return(out)


def main():
    s = sck.socket(sck.AF_INET, sck.SOCK_STREAM)
    s.bind(('192.168.0.137', 5000))
    s.listen()


    while True:
        connection, address = s.accept()
        client = Clients_class(connection, address)

        client.start()
        time.sleep(0.1)


    s.close()

if __name__ == "__main__":
    main()