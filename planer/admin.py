from django.contrib import admin

from planer.models import TodoList, Category, Employees


class TodoListAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'due_date', 'end_date')


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'color')


class EmployeesAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name',)


admin.site.register(TodoList, TodoListAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Employees, EmployeesAdmin)
