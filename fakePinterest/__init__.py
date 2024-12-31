from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
import os

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"]= os.getenv("DATABASE_URL")
app.config["SECRET_KEY"] = "dc107b82d1cb720a18c7f98f1db45619"   #Parâmetro para a criptografia da senha utilizado pelo Bcrypt
app.config["UPLOAD_FOLDER"] = "static/fotos_posts" #Caminho dpara a pasta de armazamento das fotos

database = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "homepage"

from fakePinterest import routes