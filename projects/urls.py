from django.urls import path

from . import views

app_name = 'projects'

urlpatterns = [
    path('', views.public_home, name='home'),
    path('calendario/', views.public_calendar, name='calendar'),
    path('calendario/eventos/', views.public_calendar_events, name='calendar_events'),
    path('projetos/<int:pk>/', views.public_project_detail, name='project_detail'),
    path('tarefas/', views.public_tasks, name='tasks'),
]