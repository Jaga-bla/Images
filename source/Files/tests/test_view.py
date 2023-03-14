from django.urls import reverse
from Files.models import Image, ExpiringImage
from Users.models import Permission, ThumbnailOption
from Files.serializers import ImageSerializer
from rest_framework.test import APIRequestFactory, APIClient,APITestCase 
from django.contrib.auth.models import User
from django.conf import settings
from Files.views import UserImageView,ImageUrlView, image_thumbnail_view, image_org_link_view,image_exp_link_view
from rest_framework.test import force_authenticate
from django.core.files.uploadedfile import SimpleUploadedFile

class TestApi(APITestCase):
    
    def setUp(self):
        self.factory = APIRequestFactory()
        
        self.test_user = User.objects.create(
            username = 'testuser',
            password = '1234'
            )
        ThumbnailOption.objects.create(
            size = 200
            )
        permission = Permission.objects.create(
            name = "Test Persmission",
            )
        thumbnail_options = ThumbnailOption.objects.all()
        permission.thumbnail_option.set(thumbnail_options)
        permission.save()
        self.test_user.profile.permission = permission

        self.path = '{}\{}\{}\{}'.format(settings.MEDIA_ROOT,'files',self.test_user.username,'test.png')
        
        self.image = Image.objects.create(
            name = 'test name',
            user = self.test_user,
            file = self.path
        )
        self.factory = APIRequestFactory()
        self.client = APIClient()
        
    def test_UserImageView_get_method_authenticated(self):
        view = UserImageView.as_view()
        request = self.factory.get('/images/')
        force_authenticate(request, user=self.test_user)
        response = view(request)
        images = Image.objects.filter(user = self.test_user)
        expected_data = ImageSerializer(images,context={'request': request}, many=True).data
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, expected_data)       
        
    def test_UserImageView_get_method_unauthenticated(self):
        view = UserImageView.as_view()
        request = self.factory.get('/images/')
        response = view(request)
        self.assertEqual(response.status_code, 401) 
    
    def test_UserImageView_post_method_authenticated(self):
        view = UserImageView.as_view()
        file =  SimpleUploadedFile(
                         name='test_image.jpg', 
                         content=open(self.path, 'rb').read(), content_type='image/png')
        jsondata =  {'name': 'testname', 
                     'file':file}
        json_image = ImageSerializer(jsondata)
        request = self.factory.post('/images/', json_image.data,format='json')
        force_authenticate(request, user=self.test_user)
        response = view(request)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/images/url/2/')
        
    def test_ImageUrlView_get_method(self):
        view = ImageUrlView.as_view()
        request = self.factory.get('images/url/<int:image_pk>/')
        force_authenticate(request, user=self.test_user)
        response = view(request, image_pk='1')
        response.render()
        self.assertEqual(response.status_code, 200)
        
    def test_ImageUrlView_post_method(self):
        view = ImageUrlView.as_view()
        request = self.factory.post('images/url/<int:image_pk>/', {'time_delta':400})
        force_authenticate(request, user=self.test_user)
        response = view(request, image_pk='1')
        exp_img= ExpiringImage.objects.get(pk =1)
        self.assertEqual(exp_img.time_delta, 400)
        self.assertEqual(response.status_code, 302)
        
    def test_image_thumbnail_view_with_permission(self):
        view = image_thumbnail_view
        request = self.factory.get('thumbnail/<int:size>/<int:image_pk>/')
        force_authenticate(request, user=self.test_user)
        response = view(request, size = 200, image_pk='1')
        self.assertEqual(response.status_code, 200)
    
    def test_image_thumbnail_view_no_permission(self):
        view = image_thumbnail_view
        request = self.factory.get('thumbnail/<int:size>/<int:image_pk>/')
        force_authenticate(request, user=self.test_user)
        response = view(request, size = 400, image_pk='1')
        self.assertEqual(response.status_code, 403)
        
    def test_image_org_link_view_with_permission(self):
        self.test_user.profile.permission.org_link = True
        self.test_user.profile.permission.save()
        view = image_org_link_view
        request = self.factory.get('<int:image_pk>/')
        force_authenticate(request, user=self.test_user)
        response = view(request, image_pk='1')
        self.assertEqual(response.status_code, 200)
        
    def test_image_org_link_view_no_permission(self):
        view = image_org_link_view
        request = self.factory.get('<int:image_pk>/')
        force_authenticate(request, user=self.test_user)
        response = view(request, image_pk='1')
        self.assertEqual(response.status_code, 403)
        
    def test_image_exp_link_view_with_permission(self):
        self.test_user.profile.permission.exp_link = True
        self.test_user.profile.permission.save()
        ExpiringImage.objects.create(
            original_image = self.image,
            file = self.path
        )
        view = image_exp_link_view
        request = self.factory.get('exp/link/<int:image_pk>/')
        force_authenticate(request, user=self.test_user)
        response = view(request, image_pk='1')
        self.assertEqual(response.status_code, 200)
        
    def test_image_exp_link_view_no_permission(self):
        view = image_exp_link_view
        request = self.factory.get('exp/link/<int:image_pk>/')
        force_authenticate(request, user=self.test_user)
        response = view(request, image_pk='1')
        self.assertEqual(response.status_code, 403)
        
        
        