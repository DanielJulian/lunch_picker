from flask import Flask, render_template, request, jsonify, render_template_string
from database_tools import get_db
app = Flask(__name__)


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
    result_query = "SELECT id, name, votes FROM food WHERE date=CURRENT_DATE ORDER BY name"
    cur.execute(result_query)
    insert_result_list = cur.fetchall()
    cur.close()
    context = {
        'result_list': insert_result_list
    }

    result = {
        'html': render_template('vote_options.html', **context),
    }

    return jsonify(result)


@app.route('/vote_food', methods=['POST'])
def vote_food():
    # TODO - Food ID comes by parameter. must increment food vote integer by one.
    return jsonify("Piola")


if __name__ == '__main__':
    app.run()
