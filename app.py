#Importamos las librerias
from flask import Flask, render_template, request
from mongo import MongoConnection
#Creamos la conexión a la base de datos
db_client = MongoConnection().client
db = db_client.get_database('LIBROS')
col = db.get_collection('GENERO-TERROR')
#Se está creando una instancia de la clase Flask que representa la aplicación web.
app = Flask(__name__)
#Define la ruta de la aplicación que responde a solicitud post y get
@app.route('/', methods=['GET', 'POST'])


def index():
    if request.method == 'POST':
        query = request.form['search']
        # Realizar la búsqueda en la colección MongoDB por el campo 'info_books'
        results = col.find({'info_books': {'$regex': f'.*{query}.*', '$options': 'i'}})
        return render_template('index.html', query=query, results=results)
    return render_template('index.html', query='', results=[])

if __name__ == '__main__':
    app.run(debug=True)