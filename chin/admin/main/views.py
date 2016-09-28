from . import admin
from flask import render_template, request, redirect


@admin.route('/')
def home():
    return render_template('index.html')


@admin.route('/new_task', methods=['POST'])
def new_task():
    group = request.form.get('group')
    task_name = request.form.get('task_name')
    commnd = request.form.get('command')
    args = request.form.get('args')
    valid = request.form.get('valid')
    priority = request.form.get('priority')
    rerun = request.form.get('rerun')
    rerun_times = request.form.get('rerun_times')
    machine_pool = request.form.get('machine_pool')
    father_task = request.form.get('father_task')
    scheduled_type = request.form.get('scheduled_type')
    year = request.form.get('year')
    month = request.form.get('month')
    weekday = request.form.get('weekday')
    day = request.form.get('day')
    hour = request.form.get('hour')
    minute = request.form.get('minute')
    second = request.form.get('second')

    print group, task_name, commnd, args, valid, priority, rerun, rerun_times, machine_pool, father_task, scheduled_type, year, month, weekday, day, hour, minute, second
    print 'post finish'
    return redirect('/routine_log')


@admin.route('/routine_log')
def routine_log():
    return render_template('routine_log.html')


@admin.route('/login')
def login():
    return '<h1>login</h1>'
