import datetime

from django import forms
from django.core.exceptions import ValidationError

from .models import TodoList, Category, Employees, Referats, Accredits, SetReferat


class TaskForm(forms.ModelForm):

    class Meta:
        model = TodoList
        fields = ['title', 'category', 'due_date', 'note']
        widgets = {
            'title': forms.TextInput(),
            'category': forms.Select(),
            'due_date': forms.DateInput(attrs={'id': 'datepicker'}),
            'note': forms.Textarea(attrs={'rows': 4}),
        }


class TaskEndForm(forms.ModelForm):

    class Meta:
        model = TodoList
        fields = ['end_date', 'due_date', 'note']
        labels = {
            'due_date': 'Следующий крайний срок'
        }
        widgets = {
            'end_date': forms.DateInput(attrs={'id': 'datepicker'}),
            'due_date': forms.DateInput(attrs={'id': 'due_date'}),
            'note': forms.Textarea(attrs={'rows': 3}),
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


class EmployeesForm(forms.ModelForm):

    class Meta:
        model = Employees
        fields = ['last_name', 'first_name', 'patronym', 'rank', 'is_doctor']
        widgets = {
            'last_name': forms.TextInput(attrs={'placeholder': 'Фамилия'}),
            'first_name': forms.TextInput(attrs={'placeholder': 'Имя'}),
            'patronym': forms.TextInput(attrs={'placeholder': 'Отчество'}),
            'rank': forms.TextInput(attrs={'placeholder': 'Должность'}),
            'is_doctor': forms.CheckboxInput()
        }


class ReferatForm(forms.ModelForm):

    class Meta:
        model = Referats
        fields = ['title', 'for_doctor']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Название'}),
            'for_doctor': forms.CheckboxInput()
        }


class AccreditForm(forms.ModelForm):

    class Meta:
        model = Accredits
        fields = ['title', 'first_year']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Название (период)'}),
            'first_year': forms.NumberInput(attrs={'placeholder': 'год начала аккредитации'})
        }


class AssignReferatForm(forms.ModelForm):

    class Meta:
        model = SetReferat
        fields = ['employee', 'referat', 'date']
