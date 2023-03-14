from django.test import SimpleTestCase
from django.urls import reverse, resolve
from Files import views

class TestUrls(SimpleTestCase):
    
    def test_image_list_url(self):
        url = reverse('image-list',)
        self.assertEquals(resolve(url).func.view_class, views.UserImageView)
    
    def test_url_list_url(self):
        url = reverse('url-list',args = ['1'])
        self.assertEquals(resolve(url).func.view_class, views.ImageUrlView)

    def test_thumbnail_url(self):
        url = reverse('thumbnail-url',args = ['200','1'])
        self.assertEquals(resolve(url).func, views.image_thumbnail_view)

    def test_exp_link_url(self):
        url = reverse('exp-link',args = ['1'])
        self.assertEquals(resolve(url).func, views.image_exp_link_view)

    def test_org_link_url(self):
        url = reverse('org-link',args = ['1'])
        self.assertEquals(resolve(url).func, views.image_org_link_view)