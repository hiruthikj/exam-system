# Generated by Django 3.1.3 on 2020-11-02 10:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stud_app', '0003_question_pub_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='pub_date',
            field=models.DateTimeField(verbose_name='date published'),
        ),
    ]
