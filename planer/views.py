# -*- coding: utf8 -*-
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.utils.safestring import mark_safe
from django.utils.html import conditional_escape as esc

from .forms import TaskForm, TaskEndForm, CategoryForm, EmployeesForm, ReferatForm, \
    AccreditForm, AssignReferatForm, SetReferatForm
from .models import TodoList, Category, Employees, Referats, Accredits, SetReferat
from .utils import TaskCalendar


@login_required
def todo_list(request):
    today = date.today()
    seven_days = today + timedelta(days=6)
    title = 'Скоро'
    is_ended = False
    todolist = TodoList.objects.filter(is_ended=False).order_by('due_date')
    context = {'todolist': todolist,
               'title': title,
               'is_ended': is_ended,
               'today': today,
               'seven_days': seven_days}
    return render(request, 'planer/todo_list.html', context)


@login_required
def tasks_ended(request):
    title = 'Закрытые задачи'
    is_ended = True
    todolist = TodoList.objects.filter(is_ended=True).order_by('due_date')
    context = {'todolist': todolist, 'title': title, 'is_ended': is_ended}
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
        form = TaskEndForm(instance=task)

    context = {'task': task, 'form': form}
    return render(request, 'planer/task_detail.html', context)


@login_required
def task_add(request):
    title = 'Добавить задачу'
    today = date.today()

    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('todo_list')
    else:
        form = TaskForm()
    context = {'title': title, 'form': form, 'today': today}
    return render(request, 'planer/task.html', context)


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
        form = TaskForm(instance=task)
    context = {'title': title, 'form': form, 'today': today}
    return render(request, 'planer/task.html', context)


@login_required
def category_list(request):
    titte = 'Справочник категорий'
    categories = Category.objects.all()
    context = {'categories': categories, 'titte': titte}
    return render(request, 'planer/category_list.html', context)


@login_required
def category_add(request):
    title = 'Добавить категорию'

    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('category_list')
    else:
        form = CategoryForm()

    context = {'title': title, 'form': form}
    return render(request, 'planer/category.html', context)


@login_required
def category_edit(request, category_id):
    title = 'Редактировать категорию'
    category = get_object_or_404(Category, id=category_id)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('category_list')
    else:
        form = CategoryForm(instance=category)
    context = {'title': title, 'form': form}
    return render(request, 'planer/category.html', context)


@login_required
def calendar(request, year, month):
    today = date.today()
    day = date(year, month, 1)
    prev = day + relativedelta(months=-1)
    next_month = day + relativedelta(months=+1)
    my_tasks = TodoList.objects.order_by('due_date').filter(
        due_date__year=year, due_date__month=month, is_ended=False)

    cal = TaskCalendar(my_tasks, locale='C').formatmonth(year, month)
    context = {'calendar': mark_safe(cal), 'today': today, 'prev': prev, 'next': next_month}

    return render(request, 'planer/calendar.html', context)


@login_required
def employees_list(request):
    title = 'Справочник сотрудников'
    employees = Employees.objects.all()
    context = {'title': title, 'employees': employees}
    return render(request, 'planer/employees_list.html', context)


@login_required
def employee_add(request):
    title = 'Добавить сотрудника'

    if request.method == 'POST':
        form = EmployeesForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('employees_list')
    else:
        form = EmployeesForm()

    context = {'title': title, 'form': form}
    return render(request, 'planer/employee.html', context)


def employee_edit(request, employee_id):
    title = 'Редактировать сотрудника'
    employee = get_object_or_404(Employees, id=employee_id)
    if request.method == 'POST':
        form = EmployeesForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
            return redirect('employees_list')
    else:
        form = EmployeesForm(instance=employee)
    context = {'title': title, 'form': form}
    return render(request, 'planer/employee.html', context)


@login_required
def referats_list(request):
    title = 'Справочник рефератов'
    referats = Referats.objects.all()
    context = {'title': title, 'referats': referats}
    return render(request, 'planer/referats_list.html', context)


@login_required
def referat_add(request):
    title = 'Добавить реферат'
    if request.method == 'POST':
        form = ReferatForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('referats_list')
    else:
        form = ReferatForm()
    context = {'title': title, 'form': form}
    return render(request, 'planer/referat.html', context)


@login_required
def referat_edit(request, referat_id):
    title = 'Добавить реферат'
    referat = get_object_or_404(Referats, id=referat_id)
    if request.method == 'POST':
        form = ReferatForm(request.POST, instance=referat)
        if form.is_valid():
            form.save()
            return redirect('referats_list')
    else:
        form = ReferatForm(instance=referat)
    context = {'title': title, 'form': form}
    return render(request, 'planer/referat.html', context)


@login_required
def accredits_list(request):
    title = 'Список аккредитаций'
    accredits = Accredits.objects.all()
    context = {'title': title, 'accredits': accredits}
    return render(request, 'planer/accredits_list.html', context)


@login_required
def accredit_add(request):
    title = 'Добавить аккредитацию'
    if request.method == 'POST':
        form = AccreditForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('accredits_list')
    else:
        form = AccreditForm()
    context = {'title': title, 'form': form}
    return render(request, 'planer/accredit.html', context)


@login_required
def accredit_edit(request, accredit_id):
    title = 'Редактировать аккредитацию'
    accredit = get_object_or_404(Accredits, id=accredit_id)
    if request.method == 'POST':
        form = AccreditForm(request.POST, instance=accredit)
        if form.is_valid():
            form.save()
            return redirect('accredits_list')
    else:
        form = AccreditForm(instance=accredit)
    context = {'title': title, 'form': form}
    return render(request, 'planer/accredit.html', context)


@login_required
def accredit_detail(request, accredit_id):
    accredit = get_object_or_404(Accredits, id=accredit_id)
    employees = Employees.objects.all()

    first_year = []
    second_year = []
    third_year = []
    for e in employees:
        first_year.append('<tr>')
        first_year.append('<td>')
        first_year.append(esc(e.last_name))
        first_year.append(esc(e.first_name[0]) + '.')
        first_year.append(esc(e.patronym[0]) + '.')
        first_year.append('<a href="{}'.format(reverse('assign_referat',
                                                       kwargs={'accredit_id': accredit.id,
                                                               'employee_id': e.id})))
        first_year.append('">')
        first_year.append('<span class="badge badge-success float-right"><span class="icon icon-plus">')
        first_year.append('</span></span></a>')
        first_year.append('<td>')

        second_year.append('<tr>')
        second_year.append('<td>')
        second_year.append(esc(e.last_name))
        second_year.append(esc(e.first_name[0]) + '.')
        second_year.append(esc(e.patronym[0]) + '.')
        second_year.append('<a href="{}'.format(reverse('assign_referat',
                                                        kwargs={'accredit_id': accredit.id,
                                                                'employee_id': e.id})))
        second_year.append('">')
        second_year.append('<span class="badge badge-success float-right"><span class="icon icon-plus">')
        second_year.append('</span></span></a>')
        second_year.append('<td>')

        third_year.append('<tr>')
        third_year.append('<td>')
        third_year.append(esc(e.last_name))
        third_year.append(esc(e.first_name[0]) + '.')
        third_year.append(esc(e.patronym[0]) + '.')
        third_year.append('<a href="{}'.format(reverse('assign_referat',
                                                       kwargs={'accredit_id': accredit.id,
                                                               'employee_id': e.id})))
        third_year.append('">')
        third_year.append('<span class="badge badge-success float-right"><span class="icon icon-plus">')
        third_year.append('</span></span></a>')
        third_year.append('<td>')

        for i in range(1, 13):
            first_year.append('<td>')
            for r in accredit.setreferat_set.filter(date__year=accredit.first_year, employee=e.id):
                if r.date.month == i:
                    first_year.append(esc(r.referat.title))
            first_year.append('</td>')
        first_year.append('</tr>')

        for i in range(1, 13):
            second_year.append('<td>')
            for r in accredit.setreferat_set.filter(date__year=accredit.first_year+1, employee=e.id):
                if r.date.month == i:
                    second_year.append(esc(r.referat.title))
            second_year.append('</td>')
        second_year.append('</tr>')

        for i in range(1, 13):
            third_year.append('<td>')
            for r in accredit.setreferat_set.filter(date__year=(accredit.first_year)+2, employee=e.id):
                if r.date.month == i:
                    third_year.append(esc(r.referat.title))
            third_year.append('</td>')
        third_year.append('</tr>')

    context = {'accredit': accredit, 'employees': employees,
               'first_year': first_year, 'second_year': second_year, 'third_year': third_year}
    return render(request, 'planer/accredit_detail.html', context)

@login_required
def assign_referat(request, accredit_id, employee_id):
    title = 'Назначить реферат'
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
    context = {'title': title, 'form': form,
               'accredit': accredit, 'employee': employee}
    return render(request, 'planer/assign_referat.html', context)
