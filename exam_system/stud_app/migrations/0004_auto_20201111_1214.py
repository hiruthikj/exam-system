# Generated by Django 3.1.3 on 2020-11-11 06:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('stud_app', '0003_auto_20201109_0142'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='student',
            options={'ordering': ['dept_fk__dept_name']},
        ),
        migrations.AddField(
            model_name='exam',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='course',
            name='course_desc',
            field=models.TextField(blank=True, max_length=100, null=True, verbose_name='Course Description'),
        ),
        migrations.AlterField(
            model_name='course',
            name='dept_fk',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='stud_app.department'),
        ),
        migrations.AlterField(
            model_name='exam',
            name='time_limit',
            field=models.DurationField(help_text='In what UNITS???'),
        ),
    ]