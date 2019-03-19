from django.urls import path

from . import views


urlpatterns = [
    path('', views.todo_list, name='todo_list'),
    path('tasks_ended/', views.tasks_ended, name='tasks_ended'),
    path('task/add/', views.task_add, name='task_add'),
    path('task/edit/<int:task_id>/', views.task_edit, name='task_edit'),
    path('task/detail/<int:pk>/', views.task_detail, name='task_detail'),
    path('category/list/', views.category_list, name='category_list'),
    path('category/add/', views.category_add, name='category_add'),
    # path('documents_list/', views.documents_list, name='documents_list'),
    # path('document/add/', views.document_add, name='document_add'),
    # path('document/edit/<int:document_id>/', views.document_edit, name='document_edit'),
]
