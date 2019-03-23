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

    # def performed_at(self):
    #     return self.due_date.day


class WorkoutCalendar(HTMLCalendar):

    def __init__(self, workouts):
        super(WorkoutCalendar, self).__init__()
        self.workouts = self.group_by_day(workouts)

    def formatday(self, day, weekday):
        if day != 0:
            cssclass = self.cssclasses[weekday]
            if date.today() == date(self.year, self.month, day):
                cssclass += ' today'
            if day in self.workouts:
                cssclass += ' filled'
                body = ['<ul>']
                for workout in self.workouts[day]:
                    body.append('<li>')
                    body.append('<a href="%s">' % workout.get_absolute_url())
                    body.append(esc(workout.title))
                    body.append('</a></li>')
                body.append('</ul>')
                return self.day_cell(cssclass, '%d %s' % (day, ''.join(body)))
            return self.day_cell(cssclass, day)
        return self.day_cell('noday', '&nbsp;')

    def formatmonth(self, year, month, withyear=True):
        self.year, self.month = year, month
        return super(WorkoutCalendar, self).formatmonth(year, month)

    def group_by_day(self, workouts):
        field = lambda workout: workout.due_date.day
        return dict(
            [(day, list(items)) for day, items in groupby(workouts, field)]
        )

    def day_cell(self, cssclass, body):
        return '<td class="%s">%s</td>' % (cssclass, body)
