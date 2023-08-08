# Generated by Django 4.2.4 on 2023-08-04 05:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('exchange_app', '0005_book_available'),
    ]

    operations = [
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Статус')),
            ],
        ),
        migrations.CreateModel(
            name='BookExchange',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('book_offered', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='offered_exchanges', to='exchange_app.book')),
                ('book_requested', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='requested_exchanges', to='exchange_app.book')),
                ('receiver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='received_exchanges', to=settings.AUTH_USER_MODEL)),
                ('requester', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='requested_exchanges', to=settings.AUTH_USER_MODEL)),
                ('status', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Status', to='exchange_app.status')),
            ],
        ),
    ]