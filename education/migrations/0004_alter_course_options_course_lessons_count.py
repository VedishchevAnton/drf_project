# Generated by Django 4.2.3 on 2023-07-14 14:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('education', '0003_remove_lesson_course'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='course',
            options={'ordering': ('-lessons_count',), 'verbose_name': 'Курс', 'verbose_name_plural': 'Курсы'},
        ),
        migrations.AddField(
            model_name='course',
            name='lessons_count',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='Количество уроков'),
        ),
    ]
