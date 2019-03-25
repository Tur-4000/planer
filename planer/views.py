# -*- coding: utf8 -*-
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.safestring import mark_safe

from .forms import TaskForm, TaskEndForm, CategoryForm, EmployeesForm, ReferatForm, AccreditForm, AssignReferatForm
from .models import TodoList, Category, Employees, Referats, Accredits, SetReferat
from .utils import TaskCalendar


@login_required
def todo_list(request):
    today = date.today()
    seven_days = today + timedelta(days=6)
    title = 'Скоро'
    is_ended = False
    todolist = TodoList.objects.filter(is_ended=False).order_by('due_date')
    return render(request, 'planer/todo_list.html',
                  {'todolist': todolist, 'title': title,
                   'is_ended': is_ended, 'today': today, 'seven_days': seven_days})


@login_required
def tasks_ended(request):
    title = 'Закрытые задачи'
    today = date.today()
    is_ended = True
    todolist = TodoList.objects.filter(is_ended=True).order_by('due_date')
    context = {'todolist': todolist, 'title': title, 'is_ended': is_ended, 'today': today}
    return render(request, 'planer/todo_list.html', context)


@login_required
def category_filter(request, slug):
    title = 'Скоро'
    today = date.today()
    seven_days = today + timedelta(days=6)
    is_ended = False
    todolist = TodoList.objects.filter(category__slug=slug, is_ended=False).all().order_by('due_date')
    context = {'todolist': todolist, 'title': title, 'is_ended': is_ended,
               'today': today, 'seven_days': seven_days}
    return render(request, 'planer/todo_list.html', context)


@login_required
def task_detail(request, pk):
    task = get_object_or_404(TodoList, id=pk)
    today = date.today()

    if request.method == 'POST':
        form = TaskEndForm(request.POST, instance=task)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.is_ended = True
            obj.save(update_fields=['end_date', 'is_ended'])
            if 'create_new' in request.POST:
                new_task = TodoList.objects.create(
                    title=task.title,
                    category=task.category,
                    due_date=obj.due_date,
                    note=obj.note
                )
                new_task.save()
            return redirect('todo_list')
        else:
            return render(request, 'planer/task_detail.html',
                          {'task': task, 'form': form, 'today': today})
    form = TaskEndForm(instance=task)
    return render(request, 'planer/task_detail.html',
                  {'task': task, 'form': form, 'today': today})


@login_required
def task_add(request):
    title = 'Добавить задачу'
    today = date.today()

    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
        else:
            return render(request, 'planer/task.html', {'title': title, 'form': form, 'today': today})
        return redirect('todo_list')
    else:
        form = TaskForm()
        return render(request, 'planer/task.html', {'title': title, 'form': form, 'today': today})


@login_required
def task_edit(request, task_id):
    title = 'Редактировать задачу'
    today = date.today()
    task = get_object_or_404(TodoList, id=task_id)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('todo_list')
        else:
            return render(request, 'planer/task.html',
                          {'title': title, 'form': form, 'today': today})
    form = TaskForm(instance=task)
    return render(request, 'planer/task.html',
                  {'title': title, 'form': form, 'today': today})


@login_required
def category_list(request):
    titte = 'Справочник категорий'
    today = date.today()
    categories = Category.objects.all()
    return render(request,
                  'planer/category_list.html',
                  {'categories': categories, 'titte': titte, 'today': today})


@login_required
def category_add(request):
    title = 'Добавить категорию'
    today = date.today()
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('category_list')
        else:
            return render(request, 'planer/category.html',
                          {'title': title, 'form': form, 'today': today})
    form = CategoryForm()
    return render(request, 'planer/category.html',
                  {'title': title, 'form': form, 'today': today})


@login_required
def category_edit(request, category_id):
    title = 'Редактировать категорию'
    today = date.today()
    category = get_object_or_404(Category, id=category_id)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('category_list')
        else:
            return render(request, 'planer/category.html',
                          {'title': title, 'form': form, 'today': today})
    form = CategoryForm(instance=category)
    return render(request, 'planer/category.html',
                  {'title': title, 'form': form, 'today': today})


@login_required
def calendar(request, year, month):
    today = date.today()
    day = date(year, month, 1)
    prev = day + relativedelta(months=-1)
    next_month = day + relativedelta(months=+1)
    my_tasks = TodoList.objects.order_by('due_date').filter(
        due_date__year=year, due_date__month=month, is_ended=False)

    cal = TaskCalendar(my_tasks, locale='Russian_Russia').formatmonth(year, month)
    context = {'calendar': mark_safe(cal), 'today': today, 'prev': prev, 'next': next_month}

    return render(request, 'planer/calendar.html', context)


@login_required
def employees_list(request):
    title = 'Справочник сотрудников'
    employees = Employees.objects.all()
    today = date.today()
    context = {'title': title, 'employees': employees, 'today': today}
    return render(request, 'planer/employees_list.html', context)


@login_required
def employee_add(request):
    title = 'Добавить сотрудника'
    today = date.today()

    if request.method == 'POST':
        form = EmployeesForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('employees_list')
    else:
        form = EmployeesForm()

    context = {'title': title, 'today': today, 'form': form}
    return render(request, 'planer/employee.html', context)


def employee_edit(request, employee_id):
    title = 'Редактировать сотрудника'
    today = date.today()
    employee = get_object_or_404(Employees, id=employee_id)
    if request.method == 'POST':
        form = EmployeesForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
            return redirect('employees_list')
    else:
        form = EmployeesForm(instance=employee)
    context = {'title': title, 'today': today, 'form': form}
    return render(request, 'planer/employee.html', context)


@login_required
def referats_list(request):
    title = 'Справочник рефератов'
    today = date.today()
    referats = Referats.objects.all()
    context = {'title': title, 'today': today, 'referats': referats}
    return render(request, 'planer/referats_list.html', context)


@login_required
def referat_add(request):
    title = 'Добавить реферат'
    today = date.today()
    if request.method == 'POST':
        form = ReferatForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('referats_list')
    else:
        form = ReferatForm()
    context = {'title': title, 'today': today, 'form': form}
    return render(request, 'planer/referat.html', context)


@login_required
def referat_edit(request, referat_id):
    title = 'Добавить реферат'
    today = date.today()
    referat = get_object_or_404(Referats, id=referat_id)
    if request.method == 'POST':
        form = ReferatForm(request.POST, instance=referat)
        if form.is_valid():
            form.save()
            return redirect('referats_list')
    else:
        form = ReferatForm(instance=referat)
    context = {'title': title, 'today': today, 'form': form}
    return render(request, 'planer/referat.html', context)


@login_required
def accredits_list(request):
    title = 'Список аккредитаций'
    today = date.today()
    accredits = Accredits.objects.all()
    context = {'title': title, 'today': today, 'accredits': accredits}
    return render(request, 'planer/accredits_list.html', context)


@login_required
def accredit_add(request):
    title = 'Добавить аккредитацию'
    today = date.today()
    if request.method == 'POST':
        form = AccreditForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('accredits_list')
    else:
        form = AccreditForm()
    context = {'title': title, 'today': today, 'form': form}
    return render(request, 'planer/accredit.html', context)


@login_required
def accredit_edit(request, accredit_id):
    title = 'Редактировать аккредитацию'
    today = date.today()
    accredit = get_object_or_404(Accredits, id=accredit_id)
    if request.method == 'POST':
        form = AccreditForm(request.POST, instance=accredit)
        if form.is_valid():
            form.save()
            return redirect('accredits_list')
    else:
        form = AccreditForm(instance=accredit)
    context = {'title': title, 'today': today, 'form': form}
    return render(request, 'planer/accredit.html', context)


@login_required
def accredit_detail(request, accredit_id):
    today = date.today()
    accredit = get_object_or_404(Accredits, id=accredit_id)
    employees = Employees.objects.all()
    context = {'today': today, 'accredit': accredit, 'employees': employees}
    return render(request, 'planer/accredit_detail.html', context)


@login_required
def assign_referat(request, accredit_id, employee_id):
    title = 'Назначить реферат'
    today = date.today()
    accredit = get_object_or_404(Accredits, id=accredit_id)
    employee = get_object_or_404(Employees, id=employee_id)
    if request.method == 'POST':
        form = AssignReferatForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.accredit = accredit
            obj.employee = employee
            obj.save()
            return redirect('accredit_detail', accredit_id)
    else:
        form = AssignReferatForm()
    context = {'title': title, 'today': today, 'form': form,
               'accredit': accredit, 'employee': employee}
    return render(request, 'planer/assign_referat.html', context)
