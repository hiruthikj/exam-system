# Generated by Django 3.1.3 on 2020-11-15 12:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stud_app', '0015_auto_20201115_1617'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='exam',
            name='course_fk',
        ),
    ]
