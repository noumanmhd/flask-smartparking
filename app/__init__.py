from flask import Flask 
from flask_sqlalchemy import SQLAlchemy 
from flask_login import LoginManager 
from datetime import datetime, timedelta
import datetime as dt
db = SQLAlchemy()


def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'thisismysecretkeydonotstealit'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app

def current_time():
    return int(datetime.now().strftime("%Y%m%d%H%M%S"))

def book_time():
    now = datetime.now() + timedelta(minutes=30)
    return int(now.strftime("%Y%m%d%H%M%S"))

def get_time(t):
    h = int(t[8:10])
    m = int(t[10:12])
    s = int(t[12:])
    next_time = dt.time(h, m, s)
    now = datetime.now()
    now_time = now.time()
    date = dt.date(1, 1, 1)

    now_time = dt.datetime.combine(date, now_time)
    next_time = dt.datetime.combine(date, next_time)
    r = next_time - now_time
    return  r.seconds//60, r.seconds - (r.seconds//60 * 60)

app = create_app()