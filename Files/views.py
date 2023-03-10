from .models import Image
from .serializers import ImageSerializer, ImagePreviewSerializer,ImageURLsSerializer
from rest_framework.response import Response
from django.http import FileResponse
from rest_framework.views import APIView
from rest_framework.exceptions import APIException, NotFound
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, \
    permission_classes
from rest_framework.reverse import reverse
from django.conf import settings
from .permissions import HasThumbnailPermission, HasExpirationLinkPermission, HasOriginalLinkPermission

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
    Images list entrypoint.
    - `GET` method selects user images from the database. 
    - `POST` adds new image.
    """
    permission_classes = [HasThumbnailPermission(200), HasExpirationLinkPermission, HasOriginalLinkPermission]

    serializer_class = ImageSerializer
    def get(self, request, format=None):
        images = Image.objects.filter(user = request.user)
        serializer = ImageSerializer(images,context={'request': request}, many=True)
        return Response(serializer.data)
        
    def post(self, request, *args, **kwargs):
        images = Image.objects.filter(user = request.user)
        serializer = ImageSerializer(images,context={'request': request}, many=True)
        image = request.data['file']
        Image.objects.create(file=image, user = request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
@api_view(['GET'])
def imageURLView(request,image_pk, format=None):
    """
    Image thumbnail list entrypoint.

    - `GET` method returns image thumbnail with specific height.
    """
    return Response({
        "thumbnail that's 200px in height": reverse('thumbnail-url', kwargs={'size': 200, 'image_pk':image_pk},request=request, format=format),
        "thumbnail that's 400px in height": reverse('thumbnail-url', kwargs={'size': 400, 'image_pk':image_pk},request=request, format=format),
    })
        
    
@api_view(['GET'])
@authentication_classes([])
@permission_classes([HasThumbnailPermission(200), HasExpirationLinkPermission, HasOriginalLinkPermission])
def image_preview_view(request, size, image_pk):
    """
    Image preview (thumbnail) entrypoint.

    - `GET` method returns image thumbnail with specific height.
    """
    if request.method == 'GET':
        serializer = ImagePreviewSerializer(data={'size': size})
 
        if serializer.is_valid():

            image = get_image(image_pk)
            try:
                resized_image = image.get_thumbnail(size)
                resized_image = open(resized_image, 'rb')
            except Exception as e:
                  raise APIException('Cannot resize image')
            return FileResponse(resized_image)
        return Response(serializer.errors, status=status.HTTP_200_OK)