import datetime

from django import forms
from django.core.exceptions import ValidationError

from .models import Documents, TodoList


class DocumentForm(forms.ModelForm):

    class Meta:
        model = Documents
        fields = ['document_name', 'period', 'description']
        widgets = {
            'document_name': forms.TextInput(),
            'period': forms.Select(),
            'description': forms.Textarea
        }


class TaskForm(forms.ModelForm):

    class Meta:
        model = TodoList
        fields = ['document', 'due_date', 'note']
        widgets = {
            'document': forms.Select(),
            'due_date': forms.DateInput(attrs={'type': 'date'}),
            'note': forms.Textarea(attrs={'rows': 4}),
        }


class TaskEndForm(forms.ModelForm):

    class Meta:
        model = TodoList
        fields = ['end_date', ]
        widgets = {
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean(self):
        super(TaskEndForm, self).clean()

        date = self.cleaned_data['end_date']

        if not date:
            raise ValidationError('Не установлена дата закрытия задачи')

        if date > datetime.date.today():
            raise ValidationError('Нельзя закрывать задачи будущим числом')

        start_date = self.instance.due_date

        if date < start_date:
            raise ValidationError('Задача не может быть закрыта раньше чем начата')

