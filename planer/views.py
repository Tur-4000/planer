from datetime import date, timedelta

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404, render_to_response
from django.utils.safestring import mark_safe

from .forms import TaskForm, TaskEndForm, CategoryForm
from .models import TodoList, Category, WorkoutCalendar


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
    prev = today + timedelta(days=-30)
    next = today + timedelta(days=30)
    my_tasks = TodoList.objects.order_by('due_date').filter(
        due_date__year=year, due_date__month=month, is_ended=False)
    cal = WorkoutCalendar(my_tasks).formatmonth(year, month)
    context = {'calendar': mark_safe(cal), 'today': today, 'prev': prev, 'next': next}
    return render(request, 'planer/calendar.html', context)
