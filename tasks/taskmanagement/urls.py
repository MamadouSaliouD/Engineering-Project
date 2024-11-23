from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.custom_login, name='login'),
    path('logout/', views.custom_logout, name='logout'),
    path('signup/', views.custom_signup, name='signup'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('mydashboard/', views.mydashboard, name='mydashboard'),
    path('view_task/', views.view_task, name='view_task'),
    path('task_detail/<int:task_id>/', views.task_detail, name='task_detail'),
    path('create_task/', views.create_task, name='create_task'),
    path('update_task/<int:task_id>/update/', views.update_task, name='update_task'),
    path('delete_task/<int:task_id>/delete/', views.delete_task, name='delete_task'),
    path('task/<int:task_id>/sprint/', views.sprint_view, name='sprint_view'),
    path('tasks/sprints/', views.all_sprints_view, name='all_sprints_view'),
    path('assignment_groups/', views.assignment_groups, name='assignment_groups'),
    path('create_assignment_group/', views.create_assignment_group, name='create_assignment_group'),
    path('update_assignment_group/<int:group_id>/', views.update_assignment_group, name='update_assignment_group'),
    path('delete_assignment_group/delete/<int:group_id>/', views.delete_assignment_group, name='delete_assignment_group'),
    # Add more URL patterns as needed
]
