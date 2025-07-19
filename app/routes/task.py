from flask import Blueprint, render_template,session, redirect, request, url_for, flash
from app import db
from app.models import Task


tasks_bp = Blueprint('tasks', __name__)

@tasks_bp.route('/')
def view_tasks(): #To show all the task of logged in user
    if 'user' not in session:
        return redirect(url_for('auth.login'))
    tasks = Task.query.all()
    return render_template('task.html', tasks = tasks)


@tasks_bp.route('/add', methods = ['POST'])
def add_task():
    if 'user' not in session:
        return redirect(url_for('auth.login'))

    title = request.form.get('title')
    if title :
        new_task = Task(title = title, status = 'Pending')
        db.session.add(new_task)
        db.session.commit()
        flash('Task Added Successfully', 'success')

    return redirect(url_for('tasks.view_tasks'))


@tasks_bp.route('/toggle/<int:task_id>', methods = ["POST"])
def toggle_status(task_id):
    task = Task.query.get(task_id)
    if task:
        if task.status == 'Pending':
            task.status = 'Working'
        elif task.status == 'Working':
            task.status = 'Done'
        else:
            task.status = 'Pending'
        db.session.commit()
    return redirect(url_for('tasks.view_tasks'))


@tasks_bp.route('/clear', methods = ["POST"])
def clear():
    Task.query.delete()
    db.session.commit()
    flash('All Tasks Cleared', 'info')
    return redirect(url_for('tasks.view_tasks'))
