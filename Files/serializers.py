from .models import Image, ExpiringImage
from rest_framework import serializers
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.reverse import reverse
from rest_framework.exceptions import APIException
from rest_framework.fields import CurrentUserDefault


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields =  ['file']

class ImagePreviewSerializer(serializers.Serializer):
    size = serializers.IntegerField(min_value=0)

    def validate(self, data):
        """"
        Check if user has permission to access given thumbnail size.
        """
        if data['size'] == 0:
            raise serializers.ValidationError('Size can not be zero!')
        request = self.context.get("request")
        for thumbnail_size in request.user.profile.permission.thumbnail_option.all():
            if data['size'] == thumbnail_size.size:
                return data
        raise serializers.ValidationError('You do not have a permissions to access this thumbnail.')
    
class ExpiringImageSerializer(serializers.ModelSerializer):
        class Meta:
            model = ExpiringImage
            fields =  ['time_delta']
