# Generated by Django 5.1.6 on 2025-02-20 09:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('custommodel', '0002_message'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='message',
            options={},
        ),
        migrations.AddField(
            model_name='message',
            name='user_flag',
            field=models.BooleanField(default=False),
        ),
    ]
