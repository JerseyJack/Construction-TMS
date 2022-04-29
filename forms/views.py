from datetime import datetime
from time import strptime, mktime, strftime
from flask import Blueprint, render_template, request, flash, redirect, url_for
from sqlalchemy import delete
from sqlalchemy.orm import aliased

from app import db
from registers.models import User, Task

forms = Blueprint('forms', __name__, template_folder='templates')

@forms.route('/create_task', methods=['POST', 'GET'])
def create_task():
    user_query = db.session.query(User.id, User.name).order_by(User.name)

    if request.method == 'POST':
        try:
            date_created = datetime.fromtimestamp(mktime(strptime(request.form['date_created'], '%Y-%m-%d')))
            date_required = datetime.fromtimestamp(mktime(strptime(request.form['date_required'], '%Y-%m-%d')))
            task = Task(sender_id=request.form['sender'],
                        recipient_id=request.form['recipient'],
                        subject=request.form['subject'],
                        description=request.form['description'],
                        urgency=request.form['urgency'],
                        date_created=date_created,
                        date_required=date_required)
            db.session.add(task)
            db.session.commit()
            flash('Task added successfully', 'success')
            return redirect(url_for('forms.create_task'))
        except:
            flash('Something went wrong adding a task. Please try again', 'danger')
            return render_template('task_creation.html', users=user_query)

    return render_template('task_creation.html', users=user_query)

@forms.route('/task_details/<string:task_id>', methods=['POST', 'GET'])
def task_details(task_id):
    user_query = db.session.query(User.id, User.name).order_by(User.name)
    recipient_user = aliased(User)
    sender_user = aliased(User)
    query = db.session.query(Task.id, Task.subject, Task.description, Task.urgency,
                            (recipient_user.name).label("recipient"),
                            (sender_user.name).label("sender"),
                            Task.date_created, Task.date_required, Task.date_completed) \
                            .join(recipient_user, recipient_user.id == Task.recipient_id) \
                            .join(sender_user, sender_user.id == Task.sender_id)\
                            .filter(Task.id == task_id)
    print("Query:")
    print(query.first())
    print("^^^")
    dates = {
        'date_created' : datetime.strftime(query.first().date_created, '%Y-%m-%d'),
        'date_required': datetime.strftime(query.first().date_required, '%Y-%m-%d')
    }
    if request.method == 'POST':
        try:
            task_query = db.session.query(Task).filter(Task.id == task_id).first()
            date_created = datetime.fromtimestamp(mktime(strptime(request.form['date_created'], '%Y-%m-%d')))
            date_required = datetime.fromtimestamp(mktime(strptime(request.form['date_required'], '%Y-%m-%d')))

            print("=======================")
            print(request.form['sender'])
            print(request.form['recipient'])
            print(request.form['subject'])
            print(request.form['description'])
            print(request.form['urgency'])
            print(date_created)
            print(datetime.now())
            print("=======================")

            task_query.sender_id = request.form['sender']
            task_query.request_id = request.form['recipient']
            task_query.subject = request.form['subject']
            task_query.description = request.form['description']
            task_query.urgency = request.form['urgency']
            task_query.date_created = datetime.now() #date_created
            task_query.date_required = datetime.now() #date_required

            # Check task completion
            #completed = request.form.getlist('task_completed')
            #if completed == 'checked' and task_query.date_completed is None:
            #    task_query.date_completed = datetime.now()

            db.session.commit()
            flash('Task successfully updated', 'success')
            return redirect(url_for('forms.task_register'))
        except:
            flash('Something went wrong adding a task. Please try again', 'danger')
            return redirect(url_for('forms.task_details', task_id=task_id))
    return render_template('task_details.html', users=user_query, details=query.first(), dates=dates)

@forms.route('/delete_task', methods=['POST', 'GET'])
def delete_task():
    task_id = request.form['delete_task_button']
    task_query = db.session.query(Task).filter(Task.id == task_id).first()
    db.session.delete(task_query)
    db.session.commit()
    flash('Task successfully deleted', 'success')
    return redirect(url_for('registers.task_register'))