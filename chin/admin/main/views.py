# coding=utf-8
from . import admin
from flask import render_template, request, redirect
from core.master.TaskMeta import TaskMeta
from core.models import Task
from core import DBSession
from datetime import datetime


@admin.route('/')
def home():
    return render_template('index.html')


@admin.route('/new_task', methods=['POST'])
def new_task():
    # todo: 参数校验,边界检测
    group = request.form.get('group')
    task_name = request.form.get('task_name')
    command = request.form.get('command')
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
    session = DBSession()
    a_new_task = Task(name=task_name, group=group, create_time=datetime.now(), command=command, args=args,
                      priority=priority, machine_pool=machine_pool, father_task=father_task, valid=valid,
                      rerun=rerun, rerun_times=rerun_times, scheduled_type=scheduled_type, year=year,
                      month=month, weekday=weekday, day=day, hour=hour, minute=minute, second=second)
    TaskMeta.add(a_new_task).by(session)
    session.close()

    return redirect('/')


@admin.route('/routine_log')
def routine_log():
    return render_template('routine_log.html')

