from django.contrib import admin

from planer.models import TodoList, Category


class TodoListAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'due_date', 'end_date')


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'color')


admin.site.register(TodoList, TodoListAdmin)
admin.site.register(Category, CategoryAdmin)
