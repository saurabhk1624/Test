# Generated by Django 2.0 on 2023-07-16 01:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Registartion', '0004_auto_20230715_1949'),
    ]

    operations = [
        migrations.AlterField(
            model_name='todolist',
            name='creationtime',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
