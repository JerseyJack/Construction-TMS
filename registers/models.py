import datetime
import random
from faker import Faker
from sqlalchemy import ForeignKey, or_, func
from sqlalchemy.orm import foreign
from sqlalchemy.sql.functions import Function

from app import db

class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(64))
    password = db.Column(db.String(64))
    name = db.Column(db.String(64))
    #forename = db.Column(db.String(64))
    #surname = db.Column(db.String(64))
    company = db.Column(db.String(100))
    #full_name = Function("full_name", name_get='name_get', name_set='name_set', name_del='name_del', name_expr='name_expr')

    assigned_tasks = db.relationship("Task", primaryjoin=lambda: or_(
        User.id == foreign(Task.sender_id),
        User.id == foreign(Task.recipient_id)
    ), viewonly=True)

    def to_dict(self):
        return {
            'id' : self.id,
            'username' : self.username,
            'password' : self.password,
            'name' : self.name,
            #'forename' : self.forename,
            #'surname' : self.surname,
            'company' : self.company,
            #'full_name' : self.full_name
        }

    #def name_get(self):
    #    return '{0} {1}'.format(self.forename, self.surname)

    #def name_set(self, value):
    #    self.forename, self.surname = value.split('', 1)

    #def name_del(self):
    #    self.forename = self.surname = None

    #@classmethod
    #def name_expr(cls):
    #    return func.concat(cls.forename, " ", cls.surname)

class Task(db.Model):
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

    sender_user = db.relationship("User", foreign_keys=sender_id)
    recipient_user = db.relationship("User", foreign_keys=recipient_id)

    def to_dict(self):
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
    faker = Faker()
    for i in range(n):
        user = User(username=faker.user_name(),
                    password=faker.word(),
                    name=faker.name(),
                    #forename=faker.first_name(),
                    #surname=faker.last_name(),
                    company=faker.company() )
        db.session.add(user)
    db.session.commit()
    print(f'Added {n} fake tasks to the database.')

#Create some fake tasks
def create_fake_tasks(n):
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
    db.create_all()
    #create_fake_users(50)
    #create_fake_tasks(50)

def delete_all_rows():
    User.query.delete()
    Task.query.delete()




