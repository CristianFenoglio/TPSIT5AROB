from crypt import methods
import flask
from flask import jsonify

app=flask.Flask(__name__)
app.config["DEBUG"] = True

books=[
    {
        'id':0,
        'title':'paolooo'
    },
    {
        'id':1,
        'title':'IlTitoloDelSecondoLibro'
    },
    {
        'id':3,
        'title':'Liu Cixin'
    }
]

@app.route('/api/v1/resources/books/all', methods=['GET'])
def api_all():
    return jsonify(books)

@app.route('/', methods=['GET'])
def home():
    return "<h1> Bibblioteca Online</h1><p>API</p>"
app.run()
