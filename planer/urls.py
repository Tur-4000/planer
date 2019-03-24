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
    path('employees/list/', views.employees_list, name='employees_list'),
    path('employee/add/', views.employee_add, name='employee_add'),
    path('employee/edit/<int:employee_id>/', views.employee_edit, name='employee_edit'),
    path('referats/list/', views.referats_list, name='referats_list'),
    path('referat/add/', views.referat_add, name='referat_add'),
    path('referat/edit/<int:referat_id>/', views.referat_edit, name='referat_edit'),
    path('accredits/list/', views.accredits_list, name='accredits_list'),
    path('accredit/add/', views.accredit_add, name='accredit_add'),
]
