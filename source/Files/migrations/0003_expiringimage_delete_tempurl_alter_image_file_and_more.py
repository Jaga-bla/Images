# Generated by Django 4.1.7 on 2023-03-12 19:11

import Files.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Files', '0002_remove_image_url_hash'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExpiringImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.ImageField(null=True, upload_to=Files.models.get_expiring_dir_path)),
                ('creation_date', models.DateTimeField()),
                ('time_delta', models.PositiveIntegerField()),
            ],
        ),
        migrations.DeleteModel(
            name='TempUrl',
        ),
        migrations.AlterField(
            model_name='image',
            name='file',
            field=models.ImageField(upload_to=Files.models.get_image_path),
        ),
        migrations.AddField(
            model_name='expiringimage',
            name='original_image',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='expimg', to='Files.image'),
        ),
    ]
