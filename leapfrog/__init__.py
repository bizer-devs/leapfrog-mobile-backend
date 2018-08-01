from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from leapfrog.tools import ModelEncoder

app = Flask(__name__)
app.json_encoder = ModelEncoder  # swap out the encoder for something that will attempt to call serializable()
app.config.from_pyfile('config.py')
db = SQLAlchemy(app)
migrate = Migrate(app, db)

import leapfrog.views
