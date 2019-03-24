from calendar import HTMLCalendar
from datetime import date
from itertools import groupby

from django.db import models
from django.shortcuts import reverse
from django.utils.html import conditional_escape as esc
from django.utils.text import slugify as django_slugify
from django.contrib.auth import get_user_model


User = get_user_model()


alphabet = {'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'yo', 'ж': 'zh', 'з': 'z', 'и': 'i',
            'й': 'j', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't',
            'у': 'u', 'ф': 'f', 'х': 'kh', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'shch', 'ы': 'y', 'э': 'e', 'ю': 'yu',
            'я': 'ya'}


def gen_slug(s):
    """
    Overriding django slugify that allows to use russian words as well.
    """
    new_slug = django_slugify(''.join(alphabet.get(w, w) for w in s.lower()), allow_unicode=True)
    return new_slug


class Category(models.Model):
    COLOR = (
        (1, 'blue'),
        (2, 'black'),
        (3, 'brown'),
        (4, 'darkorange'),
        (5, 'darkviolet'),
        (6, 'indigo'),
        (7, 'gray'),
        (8, 'lightblue'),
        (9, 'lawngreen'),
        (10, 'green'),
        (11, 'gold'),
        (12, 'red'),
    )

    name = models.CharField(db_index=True,
                            blank=False,
                            max_length=32,
                            verbose_name='Название')
    slug = models.SlugField(max_length=32,
                            db_index=True,
                            blank=False,
                            unique=True)
    description = models.TextField(blank=True,
                                   null=True,
                                   verbose_name='Описание')
    color = models.PositiveSmallIntegerField(choices=COLOR,
                                             db_index=True,
                                             blank=False,
                                             default=2,
                                             verbose_name='Цвет')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['name']

    def __str__(self):
        return f'{self.name}'

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = gen_slug(self.name)
        super().save(*args, **kwargs)


class TodoList(models.Model):
    title = models.CharField(db_index=True,
                             blank=False,
                             max_length=128,
                             verbose_name='Название задачи')
    due_date = models.DateField(db_index=True,
                                blank=False,
                                null=False,
                                verbose_name='Крайний срок')
    category = models.ForeignKey(Category,
                                 on_delete=models.DO_NOTHING,
                                 verbose_name='Категория',
                                 null=True)
    end_date = models.DateField(db_index=True,
                                blank=True,
                                null=True,
                                verbose_name='Дата завершения')
    is_ended = models.BooleanField(db_index=True,
                                   default=False,
                                   verbose_name='Завершена')
    note = models.TextField(blank=True,
                            null=True,
                            verbose_name='Примечание')

    class Meta:
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'

    def __str__(self):
        return f'{self.title} - {self.due_date}'

    def get_absolute_url(self):
        return reverse('task_detail', kwargs={'pk': self.id})


class Employees(models.Model):
    last_name = models.CharField(verbose_name='Фамилия',
                                 max_length=32,
                                 db_index=True,
                                 blank=False,
                                 null=False)
    first_name = models.CharField(verbose_name='Имя',
                                  max_length=32,
                                  db_index=True,
                                  blank=False,
                                  null=False)
    patronym = models.CharField(verbose_name='Отчество',
                                max_length=32,
                                blank=True,
                                null=True)
    rank = models.CharField(verbose_name='Должность',
                            max_length=64,
                            blank=False,
                            null=False)
    is_doctor = models.BooleanField(db_index=True,
                                    verbose_name='Врач',
                                    default=False)

    class Meta:
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'

    def __str__(self):
        return f'{self.last_name} {self.first_name}'


class Referats(models.Model):
    title = models.CharField(verbose_name='Название',
                             max_length=256,
                             db_index=True,
                             unique=True,
                             blank=False,
                             null=False)
    for_doctor = models.BooleanField(verbose_name='Для врачей',
                                     db_index=True,
                                     default=False)

    class Meta:
        verbose_name = 'Реферат'
        verbose_name_plural = 'Рефераты'

    def __str__(self):
        return f'{self.title}'


class Accredits(models.Model):
    title = models.CharField(verbose_name='Название (период)',
                             db_index=True,
                             max_length=128,
                             blank=False,
                             null=False,
                             unique=True)
    first_year = models.PositiveSmallIntegerField(verbose_name='Первый год',
                                                  unique=True)
    referat = models.ManyToManyField(Referats,
                                     through='SetReferat',
                                     related_name='assigned_referat')
    employee = models.ManyToManyField(Employees,
                                      through='SetReferat',
                                      related_name='assigned_employee')

    class Meta:
        verbose_name = 'Аккредитация'
        verbose_name_plural = 'Аккредитации'
        ordering = ('first_year', )

    def __str__(self):
        return f'{self.title}'


class SetReferat(models.Model):
    referat = models.ForeignKey(Referats, on_delete=models.DO_NOTHING)
    employee = models.ForeignKey(Employees, on_delete=models.DO_NOTHING)
    accredit = models.ForeignKey(Accredits, on_delete=models.DO_NOTHING)
    date = models.DateField(verbose_name='Дата реферата')

    class Meta:
        unique_together = ('referat', 'employee', 'accredit')

    def __str__(self):
        return f'{self.accredit} {self.employee} {self.referat} {self.date}'
