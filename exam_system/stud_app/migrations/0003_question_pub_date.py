# Generated by Django 3.1.3 on 2020-11-02 10:11

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('stud_app', '0002_choice_question_questionbank'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='pub_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 11, 2, 10, 11, 47, 980311, tzinfo=utc), verbose_name='date published'),
        ),
    ]