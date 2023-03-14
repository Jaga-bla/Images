from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class ThumbnailOption(models.Model):
    size = models.PositiveIntegerField()
    
    def __str__(self):
        return f"thumbnail that's {self.size}px in height"
    
class Permission(models.Model):
    name = models.CharField(
        max_length=15)
    thumbnail_option = models.ManyToManyField(
        ThumbnailOption,
        help_text='Expected options will be 200, 400 and one custom option. Additional options will not be taken into account.'
        )
    exp_link = models.BooleanField(
        default=False
        )
    org_link = models.BooleanField(
        default=False
        )
    
    def __str__(self):
        return self.name
    
class Profile(models.Model):
    user = models.OneToOneField(
        User, 
        on_delete = models.CASCADE
        )
    permission = models.ForeignKey(
        Permission, 
        null=True, 
        on_delete=models.SET_NULL
        )

    def __str__(self):
        return f'{self.user.username} Profile'

    