# Generated by Django 4.2.4 on 2023-08-15 11:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exchange_app', '0021_alter_book_condition'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='condition',
            field=models.CharField(max_length=50),
        ),
        migrations.DeleteModel(
            name='Condition',
        ),
    ]
