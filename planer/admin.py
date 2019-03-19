from django.contrib import admin

from planer.models import Documents, TodoList


class TodoListAdmin(admin.ModelAdmin):
    list_display = ('document', 'due_date', 'end_date')


admin.site.register(Documents)
admin.site.register(TodoList, TodoListAdmin)
