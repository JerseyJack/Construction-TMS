import datetime
import random
from faker import Faker
from sqlalchemy import ForeignKey, or_, func
from sqlalchemy.orm import foreign, aliased
from sqlalchemy.sql.functions import Function

from app import db

class User(db.Model):
    """
    This class creates the User model with SQLAlchemy. It also links it to the
    Task model through a foreign key relationship.
    """
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(64))
    password = db.Column(db.String(64))
    name = db.Column(db.String(64))
    company = db.Column(db.String(100))

    # Establish relationship with Task model
    assigned_tasks = db.relationship("Task", primaryjoin=lambda: or_(
        User.id == foreign(Task.sender_id),
        User.id == foreign(Task.recipient_id)
    ), viewonly=True)

    def to_dict(self):
        """
        This function converts all data from the User model into a dictionary
        :return: dictionary of model data
        """
        return {
            'id' : self.id,
            'username' : self.username,
            'password' : self.password,
            'name' : self.name,
            'company' : self.company,
        }

class Task(db.Model):
    """
    This class creates the Task model with SQLAlchemy. It also links it to the
    User model through a foreign keys.
    """
    __tablename__ = "task"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    sender_id = db.Column(db.Integer, ForeignKey('user.id'))
    recipient_id = db.Column(db.Integer, ForeignKey('user.id'))
    subject = db.Column(db.String(64))
    description = db.Column(db.Text())
    urgency = db.Column(db.String(20))
    date_created = db.Column(db.DateTime)
    date_required = db.Column(db.DateTime)
    date_completed = db.Column(db.DateTime)

    # Foreign keys
    sender_user = db.relationship("User", foreign_keys=sender_id)
    recipient_user = db.relationship("User", foreign_keys=recipient_id)

    def to_dict(self):
        """
        This function converts all data from the Task model into a dictionary
        :return: dictionary of model data
        """
        return {
            'id' : self.id,
            'sender_id' : self.sender_id,
            'recipient_id' : self.recipient_id,
            'subject' : self.subject,
            'description' : self.description,
            'urgency' : self.urgency,
            'date_created' : self.date_created,
            'date_required' : self.date_required,
            'date_completed' : self.date_completed
        }

def random_urgency():
    """
    Generates a random urgency for fake Task generator.
    :return: urgency
    """
    urgency_number = random.randint(1, 3)
    if (urgency_number == 1):
        urgency = "Low"
    else:
        if (urgency_number == 2):
            urgency = "Medium"
        else:
            urgency = "High"
    return urgency

#Create some fake users
def create_fake_users(n):
    """
    This function is used to create a specified number of fake users. It
    is used to test the table and save time creating a bunch of users.
    :param n: number of fake users to create
    :return: none
    """
    faker = Faker()
    for i in range(n):
        user = User(username=faker.user_name(),
                    password=faker.word(),
                    name=faker.name(),
                    company=faker.company() )
        db.session.add(user)
    db.session.commit()
    print(f'Added {n} fake users to the database.')

#Create some fake tasks
def create_fake_tasks(n):
    """
    This function is used to create a specified number of fake tasks. It
    is used to test the table and save time creating a bunch of tasks.
    :param n: number of fake tasks to create
    :return: none
    """
    faker = Faker()
    for i in range(n):
        task = Task(sender_id=random.randint(1, 50),
                    recipient_id=random.randint(1, 50),
                    subject=faker.sentence(nb_words=1),
                    description=faker.sentence(nb_words=20),
                    urgency=random_urgency(),
                    date_created=faker.date_between(start_date='-4m', end_date='+1m'),
                    date_required=faker.date_between(start_date='-4m', end_date='+1m'), )
        db.session.add(task)
    db.session.commit()
    print(f'Added {n} fake tasks to the database.')

def init_db():
    """
    Initialises the database models
    :return: none
    """
    db.create_all()

def create_fake_data():
    """
    Creates fake users and tasks for testing purposes.
    :return: none
    """
    create_fake_users(50)
    create_fake_tasks(50)

def delete_all_rows():
    """
    Deletes all data from user and task models. Sometimes needed
    for testing.
    :return: none
    """
    User.query.delete()
    print(f'Deleted all users from database.')
    Task.query.delete()
    print(f'Deleted all tasks from database.')
