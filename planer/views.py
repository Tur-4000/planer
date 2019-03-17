from django.shortcuts import render, redirect, get_object_or_404

from .models import Documents
from .forms import DocumentForm


def todo_list(request):
    return render(request, 'planer/todo_list.html')


def documents_list(request):
    documents = Documents.objects.all()
    return render(request,
                  'planer/list_documents.html',
                  {'documents': documents})


def document_add(request):
    title = 'Добавить новый документ'
    if request.method == 'POST':
        form = DocumentForm(request.POST)
        if form.is_valid():
            form.save()
        else:
            return render(request, 'planer/add_document.html', {'form': form, 'title': title})
        return redirect('documents_list')
    else:
        form = DocumentForm()
    return render(request,
                  'planer/add_document.html',
                  {'form': form, 'title': title})


def document_edit(request, document_id):
    title = 'Редактировать документ'
    document = get_object_or_404(Documents, id=document_id)
    if request.method == 'POST':
        form = DocumentForm(request.POST, instance=document)
        if form.is_valid():
            form.save()
        else:
            return render(request,
                          'planer/add_document.html',
                          {'form': form, 'title': title, 'document': document})
        return redirect('documents_list')
    form = DocumentForm(instance=document)
    return render(request,
                  'planer/add_document.html',
                  {'form': form, 'title': title, 'document': document})
