# Generated by Django 2.1.7 on 2019-03-18 20:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('planer', '0004_auto_20190318_2149'),
    ]

    operations = [
        migrations.AddField(
            model_name='todolist',
            name='is_ended',
            field=models.BooleanField(db_index=True, default=False, verbose_name='Завершена'),
        ),
    ]
