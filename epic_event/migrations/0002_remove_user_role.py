# Generated by Django 4.1.1 on 2022-09-28 09:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('epic_event', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='role',
        ),
    ]