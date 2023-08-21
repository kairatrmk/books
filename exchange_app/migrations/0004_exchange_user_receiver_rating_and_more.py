# Generated by Django 4.2.4 on 2023-08-18 07:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exchange_app', '0003_bookstatus'),
    ]

    operations = [
        migrations.AddField(
            model_name='exchange',
            name='user_receiver_rating',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='exchange',
            name='user_sender_rating',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]