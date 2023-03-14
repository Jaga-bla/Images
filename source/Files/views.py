from .models import Image,ExpiringImage
from rest_framework.exceptions import PermissionDenied
from .serializers import ImageSerializer, ImagePreviewSerializer, ExpiringImageSerializer
from rest_framework.response import Response
from django.http import FileResponse
from rest_framework.views import APIView
from rest_framework.exceptions import APIException, NotFound
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, \
    permission_classes
from rest_framework.reverse import reverse
from django.http import HttpResponseRedirect
from .permissions import (HasExpirationLinkPermission, 
                          HasOriginalLinkPermission, 
                          has_thumbnail_permission, 
                          custom_thumnail_permission)

def get_image_if_owner(request, image_pk):
    """
    Selects `image` from database based on its `image_pk`
    attributes.
    """
    image = None
    try:
        image = Image.objects.get(pk=image_pk)
    except Image.DoesNotExist:
        raise NotFound()
    except Exception as e:
        raise APIException()
    if request.user != image.user:
        raise APIException("You are not allowed to this file")
    return image

def get_urls_to_tb_options(request, image, format):
    """
    Returns urls to all the thumbnails user has permission to.
    """
    tb_200_px = None
    tb_400_px = None
    custom_tb = None
    if has_thumbnail_permission(request, 200):
        tb_200_px = reverse('thumbnail-url', kwargs={'size': 200, 'image_pk':image.pk},request=request, format=format)
    if has_thumbnail_permission(request, 400):
        tb_400_px = reverse('thumbnail-url', kwargs={'size': 400, 'image_pk':image.pk},request=request, format=format)
    if custom_thumnail_permission(request):
        thumnail_option_size = custom_thumnail_permission(request)
        custom_tb = reverse('thumbnail-url', kwargs={'size': thumnail_option_size, 'image_pk':image.pk},request=request, format=format)    
    return tb_200_px, tb_400_px, custom_tb

def get_url_to_org_link(request, image, format):
    """
    Returns url the original file.
    """
    original_link = None
    if request.user.profile.permission.org_link:
        original_link = reverse('org-link', kwargs={'image_pk':image.pk},request=request, format=format)
    return original_link

def get_url_to_exp_link(request, image, format):
    """
    Returns url the original file and formatted Datatime instance, 
    with values set to the time image will expire.
    """
    expiration_link, exp_time = None, None
    if request.user.profile.permission.exp_link:
        try:
            expiration_image = image.expiringimage
            exp_time = expiration_image.get_formatted_exp_time()
            expiration_link = reverse('exp-link', kwargs={'image_pk':image.pk},request=request, format=format)
        except:
            expiration_link = 'You have to generate link by POST request'
    return expiration_link, exp_time 


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
        serializer = ImageSerializer()
        image = request.data['file']
        name = request.data['name']
        if image:
            image = Image.objects.create(name = name, file=image, user = request.user)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST) 
        return HttpResponseRedirect(redirect_to=reverse('url-list', kwargs={'image_pk':image.pk}))
    
class ImageUrlView(APIView):
    """
    Images list entrypoint. - `GET` returns link to original Image file - `POST` creates ExpiringImage instance, with given number of seconds
    """
    serializer_class = ExpiringImageSerializer
         
    def get(self, request, image_pk, format=None):
        image = get_image_if_owner(request, image_pk)
        tb_200_px, tb_400_px, custom_tb = get_urls_to_tb_options(request, image, format)
        original_link = get_url_to_org_link(request, image, format)
        expiration_link, exp_time = get_url_to_exp_link(request, image, format)
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
                expiration_link,
            "expiration time":
                exp_time
        }
        return Response(data)
    
    def post(self, request, *args, **kwargs):
        serializer = ExpiringImageSerializer(data=request.data)
        image = get_image_if_owner(request, kwargs['image_pk'])
        if serializer.is_valid():
            try:
                exp_img = ExpiringImage.objects.get(original_image = image)
                exp_img.time_delta = serializer.data['time_delta']
                exp_img.save()
                return HttpResponseRedirect(redirect_to=reverse('url-list', kwargs={'image_pk':image.pk}))       
            except:
                ExpiringImage.objects.create(
                    original_image = image,
                    file = image.file,
                    time_delta = serializer.data['time_delta']
                    )            
                return HttpResponseRedirect(redirect_to=reverse('url-list', kwargs={'image_pk':image.pk}))
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view()
def image_thumbnail_view(request, size, image_pk, format = None):
    """
    Image preview (thumbnail) entrypoint. - `GET` method returns image thumbnail with specific height.
    """
    serializer = ImagePreviewSerializer
    if request.method == 'GET':
        if has_thumbnail_permission(request, size):
            serializer = ImagePreviewSerializer(data={'size': size}, context = {'request': request})
        
            if serializer.is_valid():

                image = get_image_if_owner(request, image_pk)
                try:
                    resized_image = image.get_thumbnail(size)
                    resized_image = open(resized_image, 'rb')
                except Exception as e:
                    raise APIException('Cannot resize image')
                return FileResponse(resized_image)
        raise PermissionDenied("You do not have permission to access this file.")
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view()  
@permission_classes([HasOriginalLinkPermission])  
def image_org_link_view(request, image_pk): 
    """
    - Returns image file.
    """
    image = get_image_if_owner(request, image_pk)
    return FileResponse(image.file)

@api_view()
@permission_classes([HasExpirationLinkPermission])  
def image_exp_link_view(request, image_pk): 
    
    """
    - Returns image file. Link has expiration time.
    """
    try:
        image = get_image_if_owner(request, image_pk)
        exp_image = image.expiringimage
    except Exception as e:
        raise APIException()
    if exp_image.is_expired:
        exp_image.delete()
        return Response(status=status.HTTP_404_NOT_FOUND)
    return FileResponse(exp_image.file)