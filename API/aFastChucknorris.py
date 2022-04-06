from urllib import response
import requests
cat=["animal","career","celebrity","dev","explicit","fashion","food","history","money","movie","music","political","religion","science","sport","travel"]
s=int(input("vuoi una ricerca testuale? (1/0)  >>>"))
if s:
    s=input("inserisci la/le parola/e   >>>")
    r = requests.get(f"https://api.chucknorris.io/jokes/search?query={s}")
else :
    opz=""
    for i in cat:
        opz=opz+i+"\n"
    opz=opz+"\n >>>"
    s=input(opz)
    if s in cat:
        r=requests.get(f"https://api.chucknorris.io/jokes/random?category={s}")
for i in r.json()["result"]:
    print(i["value"])