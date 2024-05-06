from django.urls import path
from . import views
from .views import create_task, delete_task, edit_task



urlpatterns =[
    path('', views.main, name='main'),
    path('task_list/', views.task_list, name="task_list"),
    path('task_list/details/<int:id>', views.details, name='details'),
    path('signup_page/', views.signup_page, name='signup_page'),
    path('logout_page/', views.logout_page, name='logout_page'),
    path('create_task/', create_task, name="create_task"),
    path('delete_task/<int:pk>', delete_task, name='delete_task'),
    path('edit_task/<int:pk>', edit_task, name='edit_task'),
    
]