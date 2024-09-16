# Generated by Django 5.1.1 on 2024-09-16 16:28

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_number', models.CharField(max_length=15, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('is_subscribed', models.BooleanField(default=False)),
            ],
        ),
    ]
