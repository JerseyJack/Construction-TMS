from flask import Blueprint, render_template, request
from sqlalchemy.orm import aliased
from registers.models import Task, User, delete_all_rows, create_fake_data
from app import db

registers = Blueprint('registers', __name__, template_folder='templates')

@registers.route('/task_register')
def task_register():
    return render_template('task_register.html', title='Task Register')

# Credit: Miguel Grinberg for tutorial on Flask Data Tables
# https://blog.miguelgrinberg.com/post/beautiful-interactive-tables-for-your-flask-templates

@registers.route('/api/data')
def task_data():
    # Use these when you want to delete all or create new data
    # delete_all_rows()
    # create_fake_data()

    # Query the task table
    recipient_user = aliased(User)
    sender_user = aliased(User)
    query = db.session.query(Task.id, Task.subject, Task.description, Task.urgency,
                            (recipient_user.name).label("recipient"),
                            (sender_user.name).label("sender"),
                            Task.date_created, Task.date_required,Task.date_completed)\
                            .join(recipient_user, recipient_user.id == Task.recipient_id)\
                            .join(sender_user, sender_user.id == Task.sender_id)

    # Search table
    search = request.args.get('search[value]')
    if search:
        query = query.filter(db.or_(
            Task.subject.like(f'%{search}%'),
            Task.urgency.like(f'%{search}%'),
            recipient_user.name.like(f'%{search}%'),
            sender_user.name.like(f'%{search}%')
        ))
    total_filtered = query.count()

    # Sorting table
    order = []
    i = 0
    while True:
        column_index = request.args.get(f'order[{i}][column]')
        print(column_index)
        if column_index is None:
            break

        column_name = request.args.get(f'columns[{column_index}][data]')
        print(column_name)
        if column_name not in ['id', 'subject', 'urgency', 'recipient', 'sender',
                               'date_created', 'date_required', 'date_completed']:
            column_name = 'id'

        descending = request.args.get(f'order[{i}][dir]') == 'desc'

        if column_name == 'recipient':
            column = 'recipient'
        else:
            if column_name == 'sender':
                column = 'sender'
            else:
                column = getattr(Task, column_name)
        print(column)

        if descending:
            column = column.desc()
        order.append(column)
        i += 1

    if order:
        query = query.order_by(*order)

    # Table paging
    start = request.args.get('start', type=int)
    length = request.args.get('length', type=int)
    query = query.offset(start).limit(length)

    # Query response
    return {
        'data' : [task._asdict() for task in query.all()],
        'recordsFiltered' : total_filtered,
        'recordsTotal' : Task.query.count(),
        'draw' : request.args.get('draw', type=int)
    }
