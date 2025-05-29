from django.urls import path
from task_app import views

app_name = 'task_app'
urlpatterns = [
    # Homepage
    path('', views.index, name='index'),

    # Page to show all tasks
    path('all_tasks/', views.all_tasks, name='all_tasks'),

    # Page to add a new task
    path('add_task/', views.add_task, name='add_task'),

    # Shows tasks due today
    path('today/', views.today, name='today'),

    # Shows tasks due this week
    path('this_week/', views.this_week, name='this_week'),

    # Page dedicated to a specific task
    path('task/<int:task_id>', views.task, name='task'),

    # Show completed tasks
    path('completed/', views.completed, name='completed'),

    # Show overdue tasks
    path('overdue/', views.overdue, name='overdue'),

    # Edits task details
    path('edit_task/<int:task_id>', views.edit_task, name='edit_task'),

    # Marks task as complete
    path('task/<int:task_id>/toggle', views.mark_complete, name='mark_complete'),

    # Adds task to today
    path('add_to_today/', views.add_to_today, name='add_to_today'),

    # Deletes a task
    path('delete_task/<int:task_id>/', views.delete_task, name='delete_task'),

    # Clears all completed tasks
    path('clear_completed/', views.clear_completed, name='clear_completed'),
]