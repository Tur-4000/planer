from django import forms

from .models import Documents


class DocumentForm(forms.ModelForm):

    class Meta:
        model = Documents
        fields = ['document_name', 'period', 'description']
        widgets = {
            'document_name': forms.TextInput(),
            'period': forms.Select(),
            'description': forms.Textarea
        }
