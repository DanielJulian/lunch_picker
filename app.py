import sqlite3
from flask import Flask, render_template, request, jsonify
from flask import g

DATABASE = 'database.sqlite3'

app = Flask(__name__)


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db


@app.route('/')
def index(name=None):
    return render_template('index.html', name=name)


@app.route('/create_poll', methods=['POST'])
def create_poll():
    # Obtengo las opciones del front end
    opcion1 = request.form['option1']
    opcion2 = request.form['option2']
    opcion3 = request.form['option3']
    opcion4 = request.form['option4']

    # Abro un puntero a la base de datos
    db = get_db()
    cur = db.cursor()

    # Creo las nuevas comidas
    query = "INSERT INTO food (name, date) VALUES ('%s', CURRENT_DATE), ('%s', CURRENT_DATE), ('%s', CURRENT_DATE), ('%s', CURRENT_DATE);" % (opcion1, opcion2, opcion3, opcion4)
    cur.execute(query)
    db.commit()
    cur.close()
    return jsonify(dict(options=[opcion1, opcion2, opcion3, opcion4]))


if __name__ == '__main__':
    app.run()
