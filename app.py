from flask import Flask, render_template, request, jsonify, redirect, abort, Response
from flask_login import LoginManager, login_user, login_required, logout_user
from database_tools import get_db
from user import User, validate_user

app = Flask(__name__)
app.config['SECRET_KEY'] = b'_5#y6L"F8Q8z\n\xec]/'

login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user):
    print(user)
    return User(user[0])


# somewhere to login
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        id = validate_user(username, password)
        if id:
            user = User(id)
            login_user(user)
            return render_template('index.html')
        else:
            return "WRONG CREDENTIALS MAI FREND"
    else:
        return render_template('login.html')


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return render_template('login.html')


@app.route('/')
@login_required
def index():
    return render_template('index.html')


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
