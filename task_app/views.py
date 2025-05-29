from django.shortcuts import render, redirect, get_object_or_404
from .models import Task
from .forms import TaskForm, TaskTodayForm
from datetime import date, datetime, timedelta, time
from django.utils.timezone import make_aware
from django.utils import timezone
from django.contrib.auth.decorators import login_required


def index(request):
    return render(request, 'task_app/index.html')


@login_required()
def all_tasks(request):
    """Display all tasks"""
    tasks = Task.objects.filter(is_complete__exact=False, owner=request.user).order_by('due_date')
    task_num = len(tasks)
    context = {'tasks': tasks, 'task_num': task_num, 'active_tab': 'all_tasks'}
    return render(request, 'task_app/all_tasks.html', context)


@login_required()
def add_task(request):
    """Adds a new task"""
    if request.method != 'POST':
        form = TaskForm()
    else:
        form = TaskForm(data=request.POST)
        if form.is_valid():
            new_task = form.save(commit=False)
            new_task.owner = request.user
            form.save()
            return redirect('task_app:all_tasks')

    context = {'form': form}
    return render(request, 'task_app/add_task.html', context)


@login_required()
def today(request):
    """Displays today's tasks"""
    today_start = make_aware(datetime.combine(date.today(), time.min))
    today_end = make_aware(datetime.combine(date.today(), time.max))

    tasks = Task.objects.filter(
        due_date__range=(today_start, today_end),
        is_complete=False, owner=request.user).order_by('due_date')
    task_num = len(tasks)

    context = {'tasks': tasks, 'active_tab': 'today', 'task_num': task_num}
    return render(request, 'task_app/today.html', context)


@login_required()
def add_to_today(request):
    if request.method != 'POST':
        form = TaskTodayForm()
    else:
        form = TaskTodayForm(request.POST)
        if form.is_valid():
            new_task = form.save(commit=False)
            new_task.owner = request.user
            form.save()
            # print("Saving due_date:", instance.due_date)
            return redirect('task_app:today')
    return render(request, 'task_app/add_to_today.html', {'form': form})


@login_required()
def this_week(request):
    """Displays tasks due this week"""
    today = date.today()
    start_of_week = today - timedelta(days=today.weekday())  # Monday
    end_of_week = start_of_week + timedelta(days=6)  # Sunday
    start_of_week_dt = make_aware(datetime.combine(start_of_week, time.min))
    end_of_week_dt = make_aware(datetime.combine(end_of_week, time.max))

    tasks_due_this_week = Task.objects.filter(
        due_date__range=(start_of_week_dt, end_of_week_dt),
        is_complete=False,
        owner=request.user).order_by('due_date')

    task_num = len(tasks_due_this_week)

    context = {'tasks': tasks_due_this_week, 'active_tab': 'this_week', 'task_num': task_num}
    return render(request, 'task_app/this_week.html', context)


@login_required()
def task(request, task_id):
    task = Task.objects.get(pk=task_id)
    context = {'task': task}
    return render(request, 'task_app/task.html', context)


@login_required()
def completed(request):
    """Shows all completed tasks"""
    tasks = Task.objects.filter(is_complete__exact=True, owner=request.user).order_by('date_completed')
    task_num = len(tasks)
    context = {'tasks': tasks, 'task_num': task_num, 'active_tab': 'completed'}
    return render(request, 'task_app/completed.html', context)


@login_required()
def overdue(request):
    """Shows overdue tasks"""
    now = timezone.now()
    tasks = Task.objects.filter(due_date__lt=now, is_complete=False, owner=request.user).order_by('due_date')
    task_num = len(tasks)

    context = {'tasks': tasks, 'active_tab': 'overdue', 'task_num': task_num}
    return render(request, 'task_app/overdue.html', context)


@login_required()
def delete_task(request, task_id):
    """Removes a task from database"""
    task = Task.objects.get(pk=task_id)
    task.delete()
    return redirect('task_app:all_tasks')


@login_required()
def clear_completed(request):
    """Clears all completed tasks"""
    tasks = Task.objects.filter(is_complete__exact=True)
    for task in tasks:
        task.delete()
    return redirect(request.META.get('HTTP_REFERER'))


@login_required()
def edit_task(request, task_id):
    """Edits task details"""
    task = Task.objects.get(pk=task_id)
    if request.method != 'POST':
        form = TaskForm(instance=task)
    else:
        form = TaskForm(instance=task, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('task_app:task', task_id)

    context = {'form': form, 'task': task}
    return render(request, 'task_app/edit_task.html', context)


@login_required()
def mark_complete(request, task_id):
    """Marks task as complete when checkbox is checked """
    if request.method == 'POST':
        task = Task.objects.get(pk=task_id)
        task.is_complete = not task.is_complete
        task.date_completed = date.today()
        task.save()
    return redirect(request.META.get('HTTP_REFERER', '/'))
