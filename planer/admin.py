from django.contrib import admin

from planer.models import Documents, TodoList, Category


class TodoListAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'due_date', 'end_date')


admin.site.register(TodoList, TodoListAdmin)
admin.site.register(Documents)
admin.site.register(Category)
