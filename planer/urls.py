from django.urls import path

from . import views


urlpatterns = [
    path('', views.todo_list, name='todo_list'),
    path('tasks/category/<slug>/', views.category_filter, name='category_filter'),
    path('tasks_ended/', views.tasks_ended, name='tasks_ended'),
    path('task/add/', views.task_add, name='task_add'),
    path('task/edit/<int:task_id>/', views.task_edit, name='task_edit'),
    path('task/detail/<int:pk>/', views.task_detail, name='task_detail'),
    path('category/list/', views.category_list, name='category_list'),
    path('category/add/', views.category_add, name='category_add'),
    path('category/edit/<int:category_id>/', views.category_edit, name='category_edit'),
    path('calendar/<int:year>/<int:month>/', views.calendar, name='calendar'),
]
