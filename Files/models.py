from django.db import models
from django.contrib.auth.models import User
from PIL import Image as Pil_img
import os
from django.conf import settings
from datetime import datetime


def get_user_dir_path(instance):
    return '{}/{}/{}'.format(settings.MEDIA_ROOT,'files',instance.user.username)

def get_expiring_dir_path(filename):
    return '{}/{}/{}/{}'.format(settings.MEDIA_ROOT,'files','expiring',filename)

def get_image_path(instance, filename):
    username = instance.user.username
    dirname = '{}/{}/{}/{}'.format(settings.MEDIA_ROOT,'files',username, filename)
    if not os.path.isdir(dirname):
        os.mkdir(dirname)
    return dirname


class Image(models.Model):
    user = models.ForeignKey(User, on_delete= models.CASCADE)
    file = models.ImageField(upload_to=get_image_path, blank=False, null=False)
    
    def get_thumbnail_name(self, size):
        """
        Generates and returns name for the thumbnail image. Returns tuple
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

        image = Pil_img.open(self.file.path)
        image = image.resize((200,size))
        if not os.path.isfile(thumbnail_name_with_path):
            image.save(thumbnail_name_with_path)

        image.close()
        
        return thumbnail_name_with_path
    
    
class ExpiringImage(models.Model):
    file = models.ImageField(upload_to=get_expiring_dir_path, blank=False, null=True)
    creation_date = models.DateTimeField()
    time_delta = models.PositiveIntegerField(min_length = 300, max_length=30000)
    
    @staticmethod
    def create(timedelta, image):
        ExpiringImage.objects.create(file = image.file, time_delta = timedelta, creation_date = datetime.now())
    
    def delete_expiring_image(self):
        self.file.delete()
    
    def check_expiration(self):
        if self.creation_date + datetime.timedelta(seconds=self.time_delta) >= datetime.now():
            self.delete_expiring_image()
            return True
        else:
            return False