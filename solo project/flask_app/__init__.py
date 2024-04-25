from flask import Flask
from flask_bcrypt import Bcrypt

app = Flask(__name__)
bcrypt = Bcrypt(app)
app.secret_key = "5e82b2e4d9d1ce5ff0032ea1916afaf229e6ea94b18c01cc260b8ae949982e67"