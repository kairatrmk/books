# Generated by Django 4.2.4 on 2023-08-07 13:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('exchange_app', '0014_exchange_user1'),
    ]

    operations = [
        migrations.AddField(
            model_name='exchange',
            name='status',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='book_status', to='exchange_app.status'),
        ),
    ]
