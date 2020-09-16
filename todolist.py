from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from datetime import datetime, timedelta
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///todo.db?check_same_thread=False')
Base = declarative_base()


class Table(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String, default='default_value')
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        return self.task


Base.metadata.create_all(engine)
session = sessionmaker(bind=engine)()
today = datetime.today()


def print_options():
    print("""1) Today's tasks
2) Week's tasks
3) All tasks
4) Missed tasks
5) Add task
6) Delete task
0) Exit""")


def print_rows(rows):
    j = 1
    for row in rows:
        print(str(j) + '. ' + row.task + '. ' + str(row.deadline.day) + ' ' + row.deadline.strftime('%b'))
        j += 1


def today_task():
    date_ = today.date()
    print("Today " + str(date_.day) + ' ' + date_.strftime('%b') + ':')
    rows = session.query(Table).filter(Table.deadline == today.date()).all()
    if len(rows) == 0:
        print('Nothing to do!')
    else:
        for row in rows:
            print(str(row.id) + '. ' + row.task)


def week_task():
    for i in range(7):
        date_ = today.date() + timedelta(days=i)
        print('')
        print(date_.strftime('%A') + ' ' + str(date_.day) + ' ' + date_.strftime('%b') + ':')
        rows = session.query(Table).filter(Table.deadline == date_).all()
        if rows:
            j = 0
            for row in rows:
                print(str(j + 1) + '. ' + row.task)
                j += 1
        else:
            print('Nothing to do!')


def all_task():
    print('All tasks:')
    rows = session.query(Table).order_by(Table.deadline).all()
    if rows:
        print_rows(rows)
    else:
        print('Nothing to do!')


def add_task():
    task = input('Enter task')
    while True:
        try:
            deadline = datetime.strptime(input('Enter deadline'), '%Y-%m-%d')
            break
        except:
            print('Deadline must be given in format YYYY-MM-DD')
    new_row = Table(task=task, deadline=deadline)
    session.add(new_row)
    session.commit()


def missed_task():
    print('')
    print('Missed tasks:')
    rows = session.query(Table).filter(Table.deadline < today.date()).order_by(Table.deadline).all()
    if rows:
        print_rows(rows)
    else:
        print('Nothing is missed!')
    print('')


def delete_task():
    print('Choose the number of the task you want to delete:')
    rows = session.query(Table).order_by(Table.deadline).all()
    if rows:
        print_rows(rows)
        no = int(input())
        session.delete(rows[no - 1])
        session.commit()
        print('The task has been deleted!')
    else:
        print('Nothing to do!')


while True:
    print_options()
    # request action
    request = int(input())
    if request not in range(0, 7):
        print('Request must be number from 0 to 6')
        continue
    if request == 0:
        break
    elif request == 1:
        today_task()
    elif request == 2:
        week_task()
    elif request == 3:
        all_task()
    elif request == 4:
        missed_task()
    elif request == 5:
        add_task()
    elif request == 6:
        delete_task()
print('Bye!')
