# Generated by Django 4.2.7 on 2023-11-14 16:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_alter_habit_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='habit',
            name='last_sending_datetime',
            field=models.DateTimeField(blank=True, default=None, null=True, verbose_name='дата и время последней отправки'),
        ),
    ]