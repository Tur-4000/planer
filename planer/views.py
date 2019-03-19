from django.shortcuts import render, redirect, get_object_or_404
import datetime
from .models import TodoList, Category
from .forms import TaskForm, TaskEndForm, CategoryForm


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


def task_detail(request, pk):
    task = get_object_or_404(TodoList, id=pk)

    if request.method == 'POST':
        form = TaskEndForm(request.POST, instance=task)
        if form.is_valid():
            task = form.save(commit=False)
            task.is_ended = True
            task.save()
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


# def documents_list(request):
#     documents = Documents.objects.all()
#     return render(request,
#                   'planer/list_documents.html',
#                   {'documents': documents})
#
#
# def document_add(request):
#     title = 'Добавить новый документ'
#     if request.method == 'POST':
#         form = DocumentForm(request.POST)
#         if form.is_valid():
#             form.save()
#         else:
#             return render(request, 'planer/add_document.html', {'form': form, 'title': title})
#         return redirect('documents_list')
#     else:
#         form = DocumentForm()
#     return render(request,
#                   'planer/add_document.html',
#                   {'form': form, 'title': title})
#
#
# def document_edit(request, document_id):
#     title = 'Редактировать документ'
#     document = get_object_or_404(Documents, id=document_id)
#     if request.method == 'POST':
#         form = DocumentForm(request.POST, instance=document)
#         if form.is_valid():
#             form.save()
#         else:
#             return render(request,
#                           'planer/add_document.html',
#                           {'form': form, 'title': title, 'document': document})
#         return redirect('documents_list')
#     form = DocumentForm(instance=document)
#     return render(request,
#                   'planer/add_document.html',
#                   {'form': form, 'title': title, 'document': document})
