from django.db import models
from django.contrib.auth.models import User
from PIL import Image as Pil_img
import os
from django.conf import settings
from datetime import timedelta
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator


def get_user_dir_path(instance):
    return '{}/{}/{}'.format(settings.MEDIA_ROOT,'files',instance.user.username)

def get_expiring_dir_path(instance, filename):
    return '{}/{}/{}'.format(settings.MEDIA_ROOT,'expiring',filename)

def get_image_path(instance, filename):
    username = instance.user.username
    dirname = '{}/{}/{}/{}/{}'.format(settings.MEDIA_ROOT,'files',username, filename, filename)
    if not os.path.isdir(dirname):
        os.mkdir(dirname)
    return dirname


class Image(models.Model):
    name = models.CharField(
        max_length=50,
        unique=True,
        null=True,
        blank=True,
        help_text='Name of the file. Must be unique.'
        )
    user = models.ForeignKey(
        User, 
        on_delete= models.CASCADE,
        help_text='User that created Image instance.'
        )
    file = models.ImageField(
        upload_to=get_image_path, 
        blank=False, 
        null=False,
        height_field='height',
        width_field='width',
        help_text='Representation of image in filesystem.'
        )
    height = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        help_text='Image height. It will be populated automatically.'
        )
    width = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        help_text='Image width. It will be populated automatically.'
        )
    
    def __str__(self):
        return self.name or f"This image has no name, PK - {self.pk}"
    
    def get_thumbnail_name(self, size):
        """
        Generates and returns name for the thumbnail image. Returns 2 variables
        where first item is thumbnail file name and second is extension.
        """
        basename = os.path.basename(self.file.name)
        filename, extension = os.path.splitext(basename)

        thumbnail_name = '{filename}__{size}'.format(
            filename=filename,
            size=size,
        )

        return thumbnail_name, extension
    
    def get_thumbnail(self, size):
        
        thumbnail_name, extension = self.get_thumbnail_name(size)
        
        thumbnail_name_with_path = os.path.join(
            get_user_dir_path(self),
            '{}{}'.format(thumbnail_name, extension),
        )
        ratio = float(size) / self.height
        width = self.width*ratio
        new_dimensions = (int(round(width)), size)
        image = Pil_img.open(self.file.path)
        image = image.resize(new_dimensions)
        if not os.path.isfile(thumbnail_name_with_path):
            image.save(thumbnail_name_with_path)

        image.close()
        
        return thumbnail_name_with_path
    
class ExpiringImage(models.Model):
    
    original_image = models.OneToOneField(
        Image, 
        on_delete=models.CASCADE, 
        related_name='expiringimage',
        help_text='Relation to original Image instance'
        )
    file = models.ImageField(
        upload_to=get_expiring_dir_path,
        blank=False, 
        null=True,
        help_text='Representation of image in filesystem.'
        )
    creation_date = models.DateTimeField(
        default=timezone.now(),
        help_text='Timestamp of creation.'
        )
    time_delta = models.IntegerField(
        default=300,
        validators=[
            MaxValueValidator(30000),
            MinValueValidator(300)
            ],
        help_text='Time in seconds. After given time, instance will be deleted, handled by view.'
        )
    
    @property
    def is_expired(self):
        if self.creation_date + timedelta(seconds=self.time_delta) <= timezone.now():
            return True
        else:
            return False
        
    def get_formatted_exp_time(self):
        date = self.creation_date + timedelta(seconds=self.time_delta)
        formatedDate = date.strftime("%Y-%m-%d %H:%M:%S")
        return formatedDate
    
    def __str__(self):
        return f"Expiring image of '{self.original_image}'"