from flask import Blueprint, render_template

navigation = Blueprint('navigation', __name__, template_folder='templates')

@navigation.route('/')
@navigation.route('/index')
def index():
    return render_template('index.html')