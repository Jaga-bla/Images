# Generated by Django 4.1.7 on 2023-03-05 18:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Files', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='image',
            name='url_hash',
        ),
    ]