from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_bootstrap import Bootstrap

app=Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///models.db'
app.config['SECRET_KEY']='210a7c7b3fdd004d1c9d2aeb'

db = SQLAlchemy(app)
bootstrap = Bootstrap(app)
app.app_context().push()

bcrypt = Bcrypt(app)

login_manager=LoginManager(app)
from master import routes