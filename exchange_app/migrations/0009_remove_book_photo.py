# Generated by Django 4.2.4 on 2023-08-25 11:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('exchange_app', '0008_bookimage'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='photo',
        ),
    ]