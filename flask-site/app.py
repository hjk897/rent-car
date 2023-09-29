import sqlite3
import datetime
import logging
import os
from flask_login import LoginManager, login_user, login_required, current_user, logout_user
from flask import Flask, render_template, request, g, flash, make_response, url_for, session, redirect
from werkzeug.security import generate_password_hash, check_password_hash
from FlaskDB import FlaskDB
from UserLogin import UserLogin

#config
DATABASE = 'tmp/app.db'
DEBUG = True



app = Flask(__name__)
app.config['SECRET_KEY'] = 'j12j#kas&@1kdsam'
app.permanent_session_lifetime = datetime.timedelta(days=10)
app.config.update(dict(DATABASE=os.path.join(app.root_path, 'app.db')))
MAX_CONTENT_LENGTH = 1024 * 1024

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = "Авторизуйтесь для доступа к закрытым страницам"
login_manager.login_message_category = "success"

def connect_db():
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn

def create_db():
    db = connect_db()
    with app.open_resource('sq_db.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()
    db.close()

def get_db():
    if not hasattr(g, 'link_db'):
        g.link_db = connect_db()
    return g.link_db

dbase = None
@app.before_request
def before_request():
    """Установление соединения с БД перед выполнением запроса"""
    global dbase
    db = get_db()
    dbase = FlaskDB(db)

@login_manager.user_loader
def load_user(user_id):
    print("load_user")
    return UserLogin().fromDB(user_id, dbase)

@app.route("/")
def index():
    return render_template('index.html', menu = dbase.getMenu())

@app.route("/login", methods=["POST", "GET"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('profile'))
    if request.method == "POST":
        user = dbase.getUserByEmail(request.form['email'])
        if user and check_password_hash(user['psw'], request.form['psw']):
            userlogin = UserLogin().create(user)
            rm = True if request.form.get('remainme') else False
            login_user(userlogin, remember=rm)
            return redirect(request.args.get("next") or url_for("profile"))
 
        flash("Неверная пара логин/пароль", "error")
 
    return render_template("login.html", menu=dbase.getMenu(), title="Авторизация")



@app.route("/register", methods=["POST", "GET"])
def register():
    if request.method == "POST":
        session.pop('_flashes', None)
        if len(request.form['name']) > 4 and len(request.form['email']) > 4  and len(request.form['contact']) == 11\
            and len(request.form['psw']) > 4 and request.form['psw'] == request.form['psw2']:
            hash = generate_password_hash(request.form['psw'])
            res = dbase.addUser(request.form['name'], request.form['contact'], request.form['email'],hash)
            if res:
                flash("Вы успешно зарегистрированы", "success")
                return redirect(url_for('login'))
            else:
                flash("Ошибка при добавлении в БД", "error")
        else:
            flash("Неверно заполнены поля", "error")
 
    return render_template("register.html", menu=dbase.getMenu(), title="Регистрация")

@app.route("/cars")
@login_required
def cars():
    return render_template("cars.html", menu=dbase.getMenu(), cars = dbase.getCarOnce(), picture = dbase.getCarOnce(),\
        title="На данной странице вы можете выбрать интересующий вас авто в аренду")


@app.route("/cars/<alias>", methods=["POST", "GET"])
@login_required
def showCar(alias):
    carid, carname, platenumber, power, picture, price, status = dbase.getCar(alias)
    if request.method == "POST":
        res = dbase.takeCar(alias, current_user.get_id(), request.form['days'])
        if not res:
            flash('Ошибка', category='error')
        else:
            flash('Машина взята в аренду', category='success')
            dbase.switchCar(alias)

            
    
    return render_template("car.html", menu=dbase.getMenu(), status=status, carname = carname,\
                                        platenumber = platenumber, power=power, price = price, picture=picture)


@app.route('/profile')
@login_required
def profile():
    carname = dbase.userCars(current_user.get_id())
    dbase.activateUser(current_user.get_id())
    return render_template("profile.html", menu=dbase.getMenu(), title="Профиль", carname=carname)

@app.route('/contact', methods=["POST", "GET"])
def contact():
        if request.method == 'POST':
            if len(request.form['username']) > 2:
                dbase.feedBack(request.form['username'], request.form['email'], request.form['message'])
                flash('Сообщение отправлено. Ответ на ваш вопрос будет отправлен на ваш email', category='success')
            else:
                flash('Ошибка отправки', category='error')
        return render_template("contact.html", menu=dbase.getMenu(), title="Обратная связь")


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Вы вышли из аккаунта", "success")
    return redirect(url_for('login'))

@app.errorhandler(404)
def PageNotFound(error):
    return render_template('page404.html', title="Страница не найдена", menu = dbase.getMenu())

if __name__ == "__main__":
        app.run(debug=True)