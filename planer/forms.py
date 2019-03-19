import datetime

from django import forms
from django.core.exceptions import ValidationError

from .models import Documents, TodoList, Category


# class DocumentForm(forms.ModelForm):
#
#     class Meta:
#         model = Documents
#         fields = ['document_name', 'period', 'description']
#         widgets = {
#             'document_name': forms.TextInput(),
#             'period': forms.Select(),
#             'description': forms.Textarea
#         }


class TaskForm(forms.ModelForm):

    class Meta:
        model = TodoList
        fields = ['title', 'category', 'due_date', 'note']
        widgets = {
            'title': forms.TextInput(),
            'category': forms.Select(),
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

        end_date = self.cleaned_data['end_date']

        if not end_date:
            raise ValidationError('Не установлена дата закрытия задачи')

        due_date = self.instance.due_date
        today = datetime.date.today()

        if today > due_date:
            if end_date > today:
                raise ValidationError('Нельзя закрывать просроченные задачи будущим числом')


class CategoryForm(forms.ModelForm):

    class Meta:
        model = Category
        fields = ['name', 'color', 'description', ]
        widgets = {
            'name': forms.TextInput(),
            'color': forms.Select(),
            'description': forms.Textarea(attrs={'rows': 3})
        }

