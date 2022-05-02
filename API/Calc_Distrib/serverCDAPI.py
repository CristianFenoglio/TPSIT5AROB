
import time as T
from flask import Flask, app, render_template, url_for, redirect, request, make_response, jsonify
from crypt import methods
import sqlite3
import random
import string



app = Flask(__name__)
#app.config["DEBUG"] = True
@app.route("/api/calcDisp/tieni", methods=['GET'])
def tieni():
    #?idOp={idOp}&ris={ris}
    idOp=int(request.args['idOp'])
    ris=request.args['ris']
    print(idOp)
    print(ris)

    con = sqlite3.connect('./calcoloDistribuitoAPI.db')
    #with sqlite3.connect('static/db.db') as con:
    cur = con.cursor()
    cur.execute(f"UPDATE operazioni SET result = {ris} WHERE id={idOp}")
    cur.execute("commit")
    rows = cur.fetchall()
    risp="appost"
    return jsonify(risp)
    

@app.route(f"/api/calcDisp/dammi", methods=['GET'])
def dammi():
   #?id={id}
    print("oaaa")
    id=int(request.args['id'])
    print(id)
    idOp, op=findOp(id)
    json = "{" + f'"idOp":{idOp},' + f'"op":"{op}"' + "}"
    print(json)
    return json

   


def findOp(idC):
    idOp=0
    op="riposo"
   
    con = sqlite3.connect('./calcoloDistribuitoAPI.db')
    #with sqlite3.connect('static/db.db') as con:
    cur = con.cursor()
    cur.execute(f"SELECT id, operazione FROM operazioni WHERE client={idC} AND result IS NULL LIMIT 1")
    rows = cur.fetchall()
    print(rows)
    if not len (rows)==0:
        for row in rows:
            idOp =int(row[0])
            op = row[1]
        
    return idOp, op

@app.route(f"/api/calcDisp/ciao", methods=['GET'])
def ciao():
    print('ciao')


if __name__ == '__main__':
    app.run(debug = True)