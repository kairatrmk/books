# Generated by Django 4.2.4 on 2023-08-15 07:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_initial'),
        ('exchange_app', '0018_rename_genr_book_genre'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exchange',
            name='user_receiver',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user1_exchanges', to='users.customuser'),
        ),
        migrations.AlterField(
            model_name='exchange',
            name='user_sender',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_exchanges', to='users.customuser'),
        ),
    ]
