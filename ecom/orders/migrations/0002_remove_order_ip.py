# Generated by Django 5.0.1 on 2024-05-22 18:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='ip',
        ),
    ]