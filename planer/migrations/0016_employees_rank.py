# Generated by Django 2.1.7 on 2019-03-24 11:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('planer', '0015_employees'),
    ]

    operations = [
        migrations.AddField(
            model_name='employees',
            name='rank',
            field=models.CharField(default='', max_length=64, verbose_name='Должность'),
            preserve_default=False,
        ),
    ]
