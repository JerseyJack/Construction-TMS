from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = '5up3r_SEcr37_K£y'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db, render_as_batch=True)

from forms.views import forms
from navigation.views import navigation
from registers.views import registers
from registers.models import init_db

app.register_blueprint(navigation)
app.register_blueprint(forms)
app.register_blueprint(registers)

if __name__ == '__main__':
    init_db()
    app.run(host='127.0.0.1', port=5000, debug=True)


