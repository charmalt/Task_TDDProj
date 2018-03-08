from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://CCHETCU3:Blue24@localhost/flaskexample'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Create database connection object
db = SQLAlchemy(app)


class list(db.Model):
    __tablename__ = "list"
    id = db.Column(db.Integer(), primary_key=True)
    task = db.Column(db.String(80), unique=True)

    def __init__(self, task):
        self.task = task
        print(self.task)

    def __repr__(self):
        return '{}'.format(self.task)


@app.route('/')
def index():
    return 'Welcome to To Do List.'


# @app.route('/add_task', methods=['POST'])
# def add_task():
#     new_task = List(request.form['task'])
#     db.session.add(new_task)
#     db.session.commit()
#     return render_template('add_task.html')


@app.route('/add_task', methods=['GET', 'POST'])
def adding_task():
    new_task = None
    if request.method == 'POST':
        new_task = list(request.form['task'])
        db.session.add(new_task)
        db.session.commit()
        return 'Added new item to Task List.'
    return render_template('add_task.html')


# @app.route('/task_list')
# def get_todo_list():
#     list = TodoList.query.all()
#     return render_template('todo_list.html', list=list)


if __name__ == '__main__':
    app.debug = True
    app.run()