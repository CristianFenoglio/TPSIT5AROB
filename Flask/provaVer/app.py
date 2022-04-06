from flask import Flask, render_template, redirect, url_for, request
import sqlite3
import socket 
import random
import string




app = Flask(__name__)
token=''.join(random.choices(string.ascii_letters + string.digits, k=30))

def findSomething(database, tab, camp, CAMPkey,MYkey):
    con = sqlite3.connect(f'{database}')
    cur = con.cursor()
    cur.execute(f'SELECT DISTINCT {camp} FROM {tab} WHERE "{CAMPkey}"="{MYkey}"')
    rows=cur.fetchall()
    print(rows)
    for row in rows :
        return row[-1]


def Search(ip, start, stop):
    start=int(start)
    stop=int(stop)
    completion = False
    con = sqlite3.connect('./database.db')
    print(ip)
    print(start)
    print(stop)
    cur = con.cursor()
    for i in range(start, stop):
        stato="chiusa"
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex((ip, i))
        if result == 0:
            stato="aperta"
        print(result)
        serviceName=findSomething("./database.db", "service", "ServiceName", "PortNumber", int(i))

        cur.execute(f'INSERT INTO TabIp (ip, porta, stato, serviceName) VALUES ("{ip}", "{i}", "{stato}","{serviceName}")')
        cur.execute("commit")
        sock.close()
   
    #with sqlite3.connect('static/db.db') as con:
    con.close()
        
    completion=True
    return completion



@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        ip = request.form['ip']
        sta = request.form['start']
        sto= request.form['stop']
        completion = Search(ip, sta, sto)
        if completion ==False:
            error = 'somethingh is gone.'
    return redirect(url_for('secret'))
    

@app.route(f'/{token}')
def secret():
    return "This is a found!"

if __name__== "__main__":
    app.run(debug=True, host="127.0.0.1")