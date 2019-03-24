# -*- coding: utf8 -*-
import locale as _locale
from calendar import HTMLCalendar, different_locale, day_abbr, month_name
from itertools import groupby
from datetime import date

from django.utils.html import conditional_escape as esc


class TaskCalendar(HTMLCalendar):

    def __init__(self, tasks, locale=None):
        super(TaskCalendar, self).__init__()
        self.tasks = self.group_by_day(tasks)
        if locale is None:
            locale = _locale.getdefaultlocale()
        self.locale = locale

    def formatday(self, day, weekday):
        if day != 0:
            cssclass = self.cssclasses[weekday]
            if date.today() == date(self.year, self.month, day):
                cssclass += ' today'
            if day in self.tasks:
                cssclass += ' filled'
                body = ['<ul>']
                for task in self.tasks[day]:
                    body.append('<li>')
                    body.append('<a href="%s">' % task.get_absolute_url())
                    body.append(esc(task.title))
                    body.append('<br>')
                    body.append('<span class="badge badge-')
                    body.append(esc(task.category.get_color_display()))
                    body.append('">')
                    body.append(esc(task.category.name))
                    body.append('</span>')
                    body.append('</a></li>')
                body.append('</ul>')
                return self.day_cell(cssclass, '%d %s' % (day, ''.join(body)))
            return self.day_cell(cssclass, day)
        return self.day_cell('noday', '&nbsp;')

    def formatweekday(self, day):
        with different_locale(self.locale):
            s = day_abbr[day]
            s = s.encode('cp1252').decode('cp1251')

        return '<th class="%s">%s</th>' % (self.cssclasses[day], s)

    def formatmonth(self, year, month, withyear=True):
        self.year, self.month = year, month
        return super(TaskCalendar, self).formatmonth(year, month)

    def formatmonthname(self, theyear, themonth, withyear=True):
        with different_locale(self.locale):
            s = month_name[themonth]
            s = s.encode('cp1252').decode('cp1251')
            if withyear:
                s = '%s %s' % (s, theyear)

        return '<tr><th colspan="7" class="month">%s</th></tr>' % s

    def group_by_day(self, tasks):
        field = lambda task: task.due_date.day
        return dict(
            [(day, list(items)) for day, items in groupby(tasks, field)]
        )

    def day_cell(self, cssclass, body):
        return '<td class="%s">%s</td>' % (cssclass, body)

