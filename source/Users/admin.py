from django.contrib import admin
from .models import Permission, ThumbnailOption, Profile

admin.site.register(Profile)
admin.site.register(Permission)
admin.site.register(ThumbnailOption)