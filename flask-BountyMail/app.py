from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csf import CSRFProtect


app = Flask(__name__)
app.config.from_object('settings')
db = SQLAlchemy(app)

csrf = CSRFPrtect(app)
