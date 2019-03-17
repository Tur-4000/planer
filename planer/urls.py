from django.urls import path

from . import views


urlpatterns = [
    path('', views.todo_list, name='todo_list'),
    path('documents_list/', views.documents_list, name='documents_list'),
    path('document/add/', views.document_add, name='document_add'),
    path('document/edit/<int:document_id>/', views.document_edit, name='document_edit'),
]
