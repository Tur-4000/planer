# Generated by Django 2.1.7 on 2019-03-24 11:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('planer', '0016_employees_rank'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employees',
            name='patronym',
            field=models.CharField(blank=True, max_length=32, null=True, verbose_name='Отчество'),
        ),
    ]