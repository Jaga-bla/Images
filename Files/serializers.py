from .models import Image
from rest_framework import serializers
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.reverse import reverse

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields =  '__all__'

class ImagePreviewSerializer(serializers.Serializer):
    size = serializers.IntegerField(min_value=0)

    def validate(self, data):

        if data['size'] == 0:
            raise serializers.ValidationError('Size can not be zero!')

        return data
    
class ImageURLsSerializer(serializers.ModelSerializer):

    url_200 = serializers.SerializerMethodField(source="get_url")
    url_400 = serializers.SerializerMethodField(source="get_url")
    url_custom = serializers.SerializerMethodField(source="get_url")
    class Meta:
            model = Image
            fields = '__all__'
            
    def get_url_200(self, obj,request):
        return reverse('thumbnail-url', kwargs={'size': 200, 'image_pk':obj.pk},request=request, format=format)
    
    def get_url_400(self, obj,request):
        return reverse('thumbnail-url', kwargs={'size': 400, 'image_pk':obj.pk},request=request, format=format)
    
    def get_url_custom(self, obj,request):
        return reverse('thumbnail-url', kwargs={'size': 1, 'image_pk':obj.pk},request=request, format=format)