# Generated by Django 4.2.4 on 2023-08-18 12:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exchange_app', '0006_book_language'),
    ]

    operations = [
        migrations.AddField(
            model_name='genre',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to='genre_photos/'),
        ),
    ]