from django.shortcuts import render, redirect, get_object_or_404
from .models import Task, AssignmentGroup, CustomUser
from .forms import TaskForm, AssignmentGroupForm, CustomUserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.utils import timezone


User = get_user_model()

#hpg6j9.Z6ZYFkcQ
from django.db.models import Q


def index(request):
    return render(request, 'index.html')

@login_required
def view_mytask(request, task_id):
    valid_statuses = ["New", "In Progress", "Done"]
    mytask = Task.objects.filter(Q(assigned_to=request.user) & Q(creator=request.user) & Q(status__in=valid_statuses))
    task = get_object_or_404(mytask, pk=task_id)
    return render(request, 'view_mytask.html', {'mytask': mytask, 'task': task})


@login_required
def sprint_view(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    stages = [
        {'name': 'New', 'active': task.status == 'New'},
        {'name': 'In Progress', 'active': task.status == 'In Progress'},
        {'name': 'Done', 'active': task.status == 'Done'}
    ]
    return render(request, 'sprint_view.html', {'task': task, 'stages': stages})


@login_required
def all_sprints_view(request):
    tasks = Task.objects.all()
    task_sprints = []

    for task in tasks:
        stages = [
            {'name': 'New', 'active': task.status == 'New'},
            {'name': 'In Progress', 'active': task.status == 'In Progress'},
            {'name': 'Done', 'active': task.status == 'Done'}
        ]
        task_sprints.append({'task': task, 'stages': stages})

    return render(request, 'all_sprints_view.html', {'task_sprints': task_sprints})



@login_required
def view_task(request):
    valid_statuses = ["New", "In Progress", "Done"]
    tasks = Task.objects.filter(Q(assigned_to=request.user) & Q(creator=request.user) & Q(status__in=valid_statuses))
    return render(request, 'view_mytask.html', {'tasks': tasks})


@login_required
def task_detail(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    return render(request, 'task_detail.html', {'task': task})

from django.contrib import messages

@login_required
def create_task(request):
    users = CustomUser.objects.all()
    assignment_groups = AssignmentGroup.objects.all()
    
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Task registered successfully!')
            return redirect('dashboard')
    else:
        form = TaskForm()

    return render(request, 'create_task.html', {
        'form': form,
        'users': users,
        'assignment_groups': assignment_groups
    })



@login_required
def update_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, 'Task updated successfully!')
            return redirect('task_detail', task_id=task.id)
        else:
            print("Form errors:", form.errors)
    else:
        form = TaskForm(instance=task)
    
    assignment_groups = AssignmentGroup.objects.all()
    users = User.objects.all()
    
    return render(request, 'update_task.html', {
        'form': form,
        'task': task,
        'assignment_groups': assignment_groups,
        'users': users,
    })



@login_required
def task_detail(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    return render(request, 'task_detail.html', {'task': task})



@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    if request.method == 'POST':
        task.delete()
        return redirect('dashboard')
    return render(request, 'dashboard.html', {'task': task})


def custom_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})



def custom_logout(request):
    logout(request)
    return redirect('login')  



def custom_signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)  # Use your custom form here
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard') 
    else:
        form = CustomUserCreationForm()  # Use your custom form here
    return render(request, 'signup.html', {'form': form})


def mydashboard(request):
    user = request.user
    assigned_tasks = Task.objects.filter(assigned_to=user)
    created_tasks = Task.objects.filter(creator=user)

    tasks_new = assigned_tasks.filter(status="New")
    tasks_in_progress = assigned_tasks.filter(status="In Progress")
    tasks_done = assigned_tasks.filter(status="Done")

    return render(request, 'mydashboard.html', {
        'tasks_new': tasks_new,
        'tasks_in_progress': tasks_in_progress,
        'tasks_done': tasks_done,
        'created_tasks': created_tasks
    })


@login_required
def dashboard(request):
    tasks_new = Task.objects.filter(status="New")
    tasks_in_progress = Task.objects.filter(status="In Progress")
    tasks_done = Task.objects.filter(status="Done")
    
    return render(request, 'dashboard.html', {
        'tasks_new': tasks_new,
        'tasks_in_progress': tasks_in_progress,
        'tasks_done': tasks_done
    })


from django.contrib.auth.decorators import user_passes_test

def superuser_required(user):
    return user.is_superuser

@user_passes_test(superuser_required)
def create_assignment_group(request):
    if request.method == 'POST':
        form = AssignmentGroupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('assignment_groups')
    else:
        form = AssignmentGroupForm()
    return render(request, 'create_assignment_group.html', {'form': form})

def update_assignment_group(request, group_id):
    group = AssignmentGroup.objects.get(id=group_id)
    if request.method == 'POST':
        form = AssignmentGroupForm(request.POST, instance=group)
        if form.is_valid():
            form.save()
            return redirect('assignment_groups')
    else:
        form = AssignmentGroupForm(instance=group)
    return render(request, 'update_assignment_group.html', {'form': form})

def delete_assignment_group(request, group_id):
    group = AssignmentGroup.objects.get(id=group_id)
    group.delete()
    return redirect('assignment_groups')

def assignment_groups(request):
    groups = AssignmentGroup.objects.all()
    return render(request, 'assignment_groups.html', {'groups': groups})