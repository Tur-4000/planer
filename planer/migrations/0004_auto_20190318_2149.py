# Generated by Django 2.1.7 on 2019-03-18 19:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('planer', '0003_todolist'),
    ]

    operations = [
        migrations.AlterField(
            model_name='todolist',
            name='end_date',
            field=models.DateField(blank=True, db_index=True, null=True, verbose_name='Дата завершения'),
        ),
    ]
