# Generated by Django 4.2.3 on 2023-07-14 14:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('education', '0004_alter_course_options_course_lessons_count'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='course',
            options={'verbose_name': 'Курс', 'verbose_name_plural': 'Курсы'},
        ),
        migrations.RemoveField(
            model_name='course',
            name='lessons_count',
        ),
    ]
