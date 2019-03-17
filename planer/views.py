from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.


def todo_list(request):
    return render(request, 'planer/todo_list.html')


def documents_list(request):
    return render(request, 'planer/list_documents.html')
