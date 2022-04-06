#import varie ed eventuali
from glob import glob
from os import access
from flask import Flask, app, render_template, url_for, redirect, request, make_response
import semaforo
import datetime
import time as T
import sqlite3 as SQL
import subprocess as sb
import string


#inizio programma

s = semaforo.semaforo()#creazione dell istanza della classe semaforo



app = Flask(__name__)

def validate(username, password):#controllo delle credenziali dell utente
    completion = False
    con = SQL.connect('./db.db')
    cur = con.cursor()
    cur.execute("SELECT * FROM Users")#prendo tutti gli utenti dal db
    rows = cur.fetchall()
    for row in rows:
        dbUser = row[0]
        dbPass = row[1]
        if dbUser == username:#trovo quello interessato dal nome
            completion = check_password(dbPass, password)#controllo
            
    return completion#return dell risultato della ricerca

def check_password(hashed_password, user_password):
    return hashed_password == user_password#controllo tra le 2 password passate

def aggMossaDatabase(user, mossa):
    #ottengo l'ora dell'azione
    date = T.ctime()#ricavo il tempo, im momento in cui l'utente fa l'accesso
    date = date.split()#prendo solo ore minuti e secondi che sono nella terza posizione
    ora = date[3]

    #creo la query come stringa che verrà eseguita in SQL 
    mex = f'INSERT INTO StopOrRestart (user, tipoDiAzione, ora) VALUES ("{user}","{mossa}","{str(ora)}")'
    con = SQL.connect('./db.db')#creo la connessione col database
    cur = con.cursor()
    cur.execute(mex)#eseguo l'update
    cur.execute("commit")
    con.close()#chiusura connesione col database


def abnormalRotation():#rotazione di luci per quando il semaforo è SPENTO
    s.giallo(1)
    s.luci_spente(1)


def normalRotation(Tr, Tv, Tg):#rotazioni di luci per quando il semaforo è acceso
    s.rosso(Tr)
    s.verde(Tv)
    s.giallo(Tg)  




@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']#prendo username dal campo
        password = request.form['password']#prendo la password dal campo
        completion = validate(username, password)#controllo delle credenziali
        if completion == False:
            error = 'Invalid Credentials. Please try again.'#se è falso nella pagnia di login, che verra ri-returnata, ci sarà una stringa di errore 
        else:
            
            #accesso alla pagina principale, per il contollo del semaforo
            resp = make_response(redirect(url_for("funzPrinc")))#redirect alla pagina primaria
            resp.set_cookie("username", username)#settaggio dei coockie con username = quello inserito dall utente, così da poter distinguere facilmente le pagine dei diversi utenti
            return resp#return della pagina

    return render_template('login.html', error=error)#in caso di non validità delle credenziali mostra la pagina di login con un messaggio di errore


    
acceso=True#la variabile che identificherà lo stato del semaforo
mossa = "accensione"#l'azione che verrà stampata/salvata
tempoRosso = 0#tempo dell accensione del verde
tempoGiallo= 0#tempo dell accensione del rosso
tempoVerde= 0 #tempo dell accensione del giallo

'''
Spegazione del funzionamento della pagina.
i cambi vanno riemiti con i valori del tempo delle luci del semaforo
con il submit essi verranno settati ai valori scelti e verrà eseguito il test
con il bottone Change lo stato del semaforo verrà cambiato e cerrà eseguito un test.
inoltre durante lo stato di spento è possibile cambiare i tempi delle varie luci ma esse funzioneranno solo al 
riaccendimdento del semaforo con il lancio del test (nel frattempo verrà visualizzato l'abnormal dopo il submit da spento)
ogni volta che viene premuto il tasto change il programma salverà l'azione e l'utente nel database 
'''

@app.route('/funzPrinc', methods=['GET', 'POST'])
def funzPrinc():#funzione 
    global acceso#la variabile che identificherà lo stato del semaforo
    global mossa#l'azione che verrà stampata/salvata
    global tempoVerde#tempo dell accensione del verde
    global tempoRosso#tempo dell accensione del rosso
    global tempoGiallo#tempo dell accensione del giallo
    user_cookie = request.cookies.get("username")#ottengo l'user che sta compiendo l'azione dai cookie (settato precedentemente al login)
    
    if request.method == 'POST':

        if request.form.get('submit') == "Submit":#se il pulsante viene premuto
            
            #prendo i valori dei tempi dai campi
            tempoRosso = int(request.form.get('tempoRosso'))
            tempoGiallo= int(request.form.get('tempoGiallo'))
            tempoVerde = int(request.form.get('tempoVerde'))
        
        if request.form.get('Change') == "Change":#se il pulsante viene premuto
            acceso=not(acceso)#inversione del valore logico della varibile dato dalla pressione del bottone Change
            mossa="spegnimento"
            if acceso:
                mossa = "accensione"#cambio della mossa
            aggMossaDatabase(user_cookie, mossa)#aggiorno il database delle varie mosse(ovvero acceso e spento)
            print(mossa+"...")#solo una print per controllare l'azionamento
       
        if acceso == True:#azione del semaforo (sequenza di luci corretta se acceso--> normale, se spento -->abnormal)
            normalRotation(tempoGiallo, tempoVerde, tempoRosso)#rotazione di luci da acceso
        else:
            abnormalRotation()#rotazione di luci da spento

        


        return render_template('funzPrinc.html',  solution=mossa[:4])#retun della pagina + stato del semaforo
    return render_template('funzPrinc.html')


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1')