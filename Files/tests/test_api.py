from django.test import TestCase
from django.urls import reverse
from Files.models import Image
from Files.serializers import ImageSerializer
from rest_framework.test import APIRequestFactory, APIClient
from django.contrib.auth.models import User
from django.conf import settings

class TestApi(TestCase):
    
    def SetUp(self):
        self.factory = APIRequestFactory()
        
        self.test_user = User.objects.create(
            username = 'testuser',
            password = '1234')

        self.path = '{}\{}\{}\{}'.format(settings.MEDIA_ROOT,'files',self.test_user.username,'test.png')
        
        self.image = Image.objects.create(
            name = 'test name',
            user = self.test_user,
            file = self.path
        )
        
        self.client = APIClient()
        self.client.login(username='testuser', password='1234')

    def test_url_list_url(self):
        url = reverse('image-list')
        response = self.client.get(url)
        user = User.objects.filter(username = 'testuser').first()
        images = Image.objects.filter(user = user)
        expected_data = ImageSerializer(images, many=True).data
        print(expected_data)
        self.assertEqual(response.data, expected_data)
        self.assertEqual(response.status_code, 200)