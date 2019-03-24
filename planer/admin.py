from django.contrib import admin

from planer.models import TodoList, Category, Employees, Referats


class TodoListAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'due_date', 'end_date')


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'color')


class EmployeesAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name',)


class ReferatsAdmin(admin.ModelAdmin):
    list_display = ('title', 'for_doctor')


admin.site.register(TodoList, TodoListAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Employees, EmployeesAdmin)
admin.site.register(Referats, ReferatsAdmin)
