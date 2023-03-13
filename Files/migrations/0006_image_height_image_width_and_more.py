# Generated by Django 4.1.7 on 2023-03-13 16:35

import Files.models
import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Files', '0005_image_name_alter_expiringimage_creation_date_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='image',
            name='height',
            field=models.PositiveSmallIntegerField(blank=True, help_text='Image height. It will be populated automatically.', null=True),
        ),
        migrations.AddField(
            model_name='image',
            name='width',
            field=models.PositiveSmallIntegerField(blank=True, help_text='Image width. It will be populated automatically.', null=True),
        ),
        migrations.AlterField(
            model_name='expiringimage',
            name='creation_date',
            field=models.DateTimeField(default=datetime.datetime(2023, 3, 13, 16, 35, 2, 82934, tzinfo=datetime.timezone.utc), help_text='Timestamp of creation.'),
        ),
        migrations.AlterField(
            model_name='image',
            name='file',
            field=models.ImageField(height_field='height', help_text='Representation of image in filesystem.', upload_to=Files.models.get_image_path, width_field='width'),
        ),
    ]
