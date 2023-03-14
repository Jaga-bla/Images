from django.test import TestCase
from Files.models import Image, ExpiringImage
from django.contrib.auth.models import User
from django.conf import settings
from PIL import Image as Pil_img
from datetime import timedelta

class TestImageModel(TestCase):
    def setUp(self):
        self.test_user = User.objects.create(
        username = 'testuser',
        password = '1234')

        self.path = '{}\{}\{}\{}'.format(settings.MEDIA_ROOT,'files',self.test_user.username,'test.png')
        
        self.image = Image.objects.create(
            name = 'test name',
            user = self.test_user,
            file = self.path
        )
    
    def test_image_creation(self):
        self.assertEqual(self.image.file.path, self.path)
        
    def test_get_thumbnail_name(self):
        thumbnail_name, extension = self.image.get_thumbnail_name(200)
        self.assertEqual(thumbnail_name, 'test__200')
        self.assertEqual(extension, '.png')
        
    def test_get_thumbnail_path(self):
        thumbnail_name_with_path = self.image.get_thumbnail(200)
        test_path = '{}/{}/{}\{}'.format(settings.MEDIA_ROOT,'files','testuser', 'test__200.png')
        self.assertEqual(thumbnail_name_with_path, test_path)
        
    def test_thumbnail_size(self):
        thumbnail_name_with_path = self.image.get_thumbnail(200)
        thumbnail_file = Pil_img.open(open(thumbnail_name_with_path, 'rb'))
        self.assertEqual(thumbnail_file.height, 200)
        
    def test_exiring_image_is_expired_false(self):
        exp_img = ExpiringImage.objects.create(
            original_image = self.image,
            file = self.image.file.path,
            time_delta = 300
        ) 
        self.assertEqual(exp_img.is_expired, False)
        
    def test_exiring_image_is_expired_true(self):
        exp_img = ExpiringImage.objects.create(
            original_image = self.image,
            file = self.image.file.path,
            time_delta = 300
        ) 
        exp_img.creation_date = exp_img.creation_date - timedelta(seconds=301)
        exp_img.save()  
        self.assertEqual(exp_img.is_expired, True)
        
    
    
    
        
        