import requests as rq
from flask import jsonify
import time as T
import random



def main():
    id=int(input("pls dimmi l'id:  "))
    while True:

        opers = rq.get(f"http://127.0.0.1:5000/api/calcDisp/dammi?id={id}")
       
        for sens in opers.json():
            print(f"{sens}: {opers.json()[sens]}")
    
        idOp = opers .json()['idOp']
        op = opers .json()['op']
        if op=="riposo":
            break
        ris=eval(op)
        
        invia = rq.get(f'http://127.0.0.1:5000/api/calcDisp/tieni?idOp={idOp}&ris={ris}')

        




if __name__ == "__main__":
    main()