from flask import Blueprint, render_template

forms = Blueprint('forms', __name__, template_folder='templates')

@forms.route('/create_task')
def create_task():
    return render_template('task_creation.html')