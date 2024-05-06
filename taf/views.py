from django.shortcuts import render, redirect, get_object_or_404, redirect
from django.http import HttpResponse
from django.template import loader
from . models import Task
from django.contrib.auth.forms import UserCreationForm
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.views.generic.edit import CreateView, DeleteView
from django.urls import reverse_lazy
from .forms import TaskForm
# Create your views here.



def task_list(request):
    tasks =Task.objects.all().values()
    template =loader.get_template('taf/task_list.html')
    context ={
        'tasks':tasks
    }
    return render(request, 'taf/task_list.html', context)



def details(request, id):
    task = Task.objects.get(id=id)
    template = loader.get_template('taf/details.html')
    context = {
        'task': task,
    }
    return HttpResponse(template.render(context, request))


@csrf_exempt
def signup_page(request):
    template = loader.get_template('taf/signup_page.html')
    if request.method =='POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            # Log the user in if needed
            return redirect('task_list')  # Assuming 'task_list' is a valid URL name
    else:
        form = UserCreationForm()
    context ={
        'form': form
    }
    return HttpResponse(template.render(context, request))



def logout_page(request):
    logout(request)
    template = loader.get_template('taf/signup_page.html')
    return HttpResponse(template.render())

"""
def create_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = TaskForm()
    template = loader.get_template('taf/create_task.html')
    context = {
        'form': form
    }
    return render(request, 'taf/create_task.html', context)
"""
def create_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            # Associate the current user with the task
            task = form.save(commit=False)
            task.user = request.user  # Assign the current user
            task.save()
            return redirect('task_list')
    else:
        form = TaskForm()
    context = {
        'form': form
    }
    return render(request, 'taf/create_task.html', context)


def edit_task(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = TaskForm(instance=task)
    template = loader.get_template('taf/edit_task.html')
    context = {
        'form': form
    }
    return render(request, 'taf/edit_task.html', context)

def delete_task(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        task.delete()
        return redirect('task_list')
    template = loader.get_template('taf/task_confirm_delete.html')
    context = {
        'task': task
    }
    return HttpResponse(template.render(context, request))

def main(request):
    task_id = request.GET.get('id')
    if task_id is not None:
        try:
            task = Task.objects.get(id=task_id)
        except Task.DoesNotExist:
            task = None
    else:
        task = None

    context = {
        'task': task,
    }
    return render(request, 'taf/main.html', context)