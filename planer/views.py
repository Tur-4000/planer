import datetime

from django.shortcuts import render, redirect, get_object_or_404

from .forms import TaskForm, TaskEndForm, CategoryForm
from .models import TodoList, Category


def todo_list(request):
    today = datetime.date.today()
    title = 'Скоро'
    is_ended = False
    todolist = TodoList.objects.filter(is_ended=False).order_by('due_date')
    return render(request, 'planer/todo_list.html',
                  {'todolist': todolist, 'title': title, 'is_ended': is_ended, 'today': today})


def tasks_ended(request):
    title = 'Закрытые задачи'
    is_ended = True
    todolist = TodoList.objects.filter(is_ended=True).order_by('due_date')
    return render(request, 'planer/todo_list.html',
                  {'todolist': todolist, 'title': title, 'is_ended': is_ended})


def category_filter(request, slug):
    today = datetime.date.today()
    title = 'Скоро'
    is_ended = False
    todolist = TodoList.objects.filter(category__slug=slug, is_ended=False).all()
    return render(request, 'planer/todo_list.html',
                  {'todolist': todolist, 'title': title, 'is_ended': is_ended, 'today': today})


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
            return render(request, 'planer/task_detail.html',
                          {'task': task, 'form': form})
    form = TaskEndForm(instance=task)
    return render(request, 'planer/task_detail.html',
                  {'task': task, 'form': form})


def task_add(request):
    title = 'Добавить задачу'

    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
        else:
            return render(request, 'planer/task.html', {'title': title, 'form': form})
        return redirect('todo_list')
    else:
        form = TaskForm()
        return render(request, 'planer/task.html', {'title': title, 'form': form})


def task_edit(request, task_id):
    title = 'Редактировать задачу'
    task = get_object_or_404(TodoList, id=task_id)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('todo_list')
        else:
            return render(request, 'planer/task.html',
                          {'title': title, 'form': form})
    form = TaskForm(instance=task)
    return render(request, 'planer/task.html',
                  {'title': title, 'form': form})


def category_list(request):
    titte = 'Справочник категорий'
    categories = Category.objects.all()
    return render(request,
                  'planer/category_list.html',
                  {'categories': categories, 'titte': titte})


def category_add(request):
    title = 'Добавить категорию'
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('category_list')
        else:
            return render(request, 'planer/category.html',
                          {'title': title, 'form': form})
    form = CategoryForm()
    return render(request, 'planer/category.html',
                  {'title': title, 'form': form})


def category_edit(request, category_id):
    title = 'Редактировать категорию'
    category = get_object_or_404(Category, id=category_id)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('category_list')
        else:
            return render(request, 'planer/category.html',
                          {'title': title, 'form': form})
    form = CategoryForm(instance=category)
    return render(request, 'planer/category.html',
                  {'title': title, 'form': form})
