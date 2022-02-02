
from django.urls import path
from django.shortcuts import render, HttpResponseRedirect, get_object_or_404
from .models import Task



def view_task(request, pk):
    task = get_object_or_404(Task, pk=pk)
    return render(request, 'view_task.html', {
        'task': task
    })

def tasks_view(request):
    tasks = Task.objects.filter(completed=False, deleted=False).order_by('-created_date')
    return render(request, 'tasks.html', {
        'tasks': tasks
    })

def completed_tasks_view(request):
    completed_tasks = Task.objects.filter(completed=True, deleted=False).order_by('-created_date')
    return render(request, 'completed_tasks.html', {
        'tasks': completed_tasks
    })

def add_new_task(request):
    title = request.GET.get('task')
    description = request.GET.get('description') or " "
    Task.objects.create(title=title, description=description)
    return HttpResponseRedirect('/tasks/')

def delete_task(request, pk):
    task = get_object_or_404(Task, pk=pk)
    task.deleted = True
    task.save()
    return HttpResponseRedirect('/tasks/')

def complete_task(request, pk):
    task = get_object_or_404(Task, pk=pk)
    task.completed = True
    task.save()
    return HttpResponseRedirect('/tasks/')

def all_tasks(request):
    return render(request, 'all_tasks.html', {
        "pending_tasks": Task.objects.filter(completed=False, deleted=False).order_by('-created_date'),
        "completed_tasks": Task.objects.filter(completed=True, deleted=False).order_by('-created_date')
    })

urlpatterns = [
    path('tasks/', tasks_view, name='all-tasks'),
    path('tasks/<int:pk>/', view_task, name='view-task'),
    path('completed_tasks/', completed_tasks_view, name='completed-tasks'),
    path('add-task/', add_new_task, name="add-task"),
    path('delete-task/<int:pk>/', delete_task, name="delete-task"),
    path('complete_task/<int:pk>/', complete_task, name="complete-task"),
    path('all_tasks/', all_tasks, name="all-tasks"),
]
