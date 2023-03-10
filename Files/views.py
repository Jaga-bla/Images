from .models import Image, get_image_path
from .serializers import ImageSerializer, ImagePreviewSerializer
from rest_framework.response import Response
from django.http import FileResponse
from rest_framework.views import APIView
from rest_framework.exceptions import APIException, NotFound
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, \
    permission_classes
from rest_framework.reverse import reverse
from django.conf import settings
from .permissions import HasExpirationLinkPermission, HasOriginalLinkPermission
from django.http import HttpResponseRedirect

def get_image(image_pk):
    """
    Selects `image` from database based on its `image_path`
    attributes.
    """
    image = None
    try:
        image = Image.objects.get(pk=image_pk)
    except Image.DoesNotExist:
        raise NotFound()
    except Exception as e:
        raise APIException()
    return image


class UserImageView(APIView):
    """
    Images list entrypoint. - `GET` method selects user images from the database. - `POST` adds new image.
    """
    
    serializer_class = ImageSerializer
    def get(self, request, format=None):
        images = Image.objects.filter(user = request.user)
        serializer = ImageSerializer(images,context={'request': request}, many=True)
        return Response(serializer.data)
        
    def post(self, request, *args, **kwargs):
        image = request.data['file']
        image = Image.objects.create(file=image, user = request.user)
        
        return HttpResponseRedirect(redirect_to=reverse('url-list', kwargs={'image_pk':image.pk}))
    
@api_view(['GET'])
def imageURLView(request,image_pk, format=None):
    """
    Image thumbnail list entrypoint.

    - `GET` method returns image thumbnail with specific height.
    """
    try:
        image = Image.objects.get(pk=image_pk, user = request.user)
    except Exception as e:
        raise APIException('You are not allowed to this image')
    tb_200_px = None
    tb_400_px = None
    custom_tb = None
    original_link = None
    for thumnail_option in request.user.profile.permission.thumbnail_option.all():
        if thumnail_option.size == 200:
            tb_200_px = reverse('thumbnail-url', kwargs={'size': 200, 'image_pk':image_pk},request=request, format=format)
        if thumnail_option.size == 400:
            tb_400_px = reverse('thumbnail-url', kwargs={'size': 400, 'image_pk':image_pk},request=request, format=format)
        if thumnail_option.size == 1:
            custom_tb = reverse('thumbnail-url', kwargs={'size': 1, 'image_pk':image_pk},request=request, format=format)    
    if request.user.profile.permission.org_link:
        original_link = request.build_absolute_uri(image.file.url)
        
    data = {
        "thumbnail that's 200px in height": 
            tb_200_px,
        "thumbnail that's 400px in height": 
            tb_400_px,
        "thumbnail with custom height": 
            custom_tb,
        "original link": 
            original_link,
        "expiring link": 
            reverse('exp-link'),
    }
    
    return Response(data)
    
@api_view(['GET'])
def image_preview_view(request, size, image_pk):
    """
    Image preview (thumbnail) entrypoint.

    - `GET` method returns image thumbnail with specific height.
    """
    try:
        image = Image.objects.get(pk=image_pk, user = request.user)
    except Exception as e:
        raise APIException('You are not allowed to this image')
    
    if request.method == 'GET':
        serializer = ImagePreviewSerializer(data={'size': size}, context = {'request': request})
 
        if serializer.is_valid():

            image = get_image(image_pk)
            try:
                resized_image = image.get_thumbnail(size)
                resized_image = open(resized_image, 'rb')
            except Exception as e:
                  raise APIException('Cannot resize image')
            return FileResponse(resized_image)
        return Response(serializer.errors, status=status.HTTP_200_OK)
    
@api_view(['GET'])
def expiring_link_view():
    pass