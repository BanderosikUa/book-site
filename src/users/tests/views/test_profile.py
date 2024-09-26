from django.test import Client, TestCase
from django.urls import reverse

from users.models import User
from books.models import Book, UserBookRelation

class TestProfileViews(TestCase):

    @classmethod
    def setUp(cls):
        cls.client = Client()

        cls.model1 = Book.objects.create(name='some book')
        cls.user = User.objects.create_user(username='user1', password='username123', email='admifn@gmail.com')
        cls.profile = cls.user.profile


    def test_logined_profile_view_GET(self):
        self.client.force_login(self.user)
        url = reverse('profile', args=(self.user.slug,))
        response = self.client.get(url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/profile_page.html')
        
    def test_not_found_profile_view_GET(self):
        url = reverse('profile', args=('asdasdas',))
        response = self.client.get(url)
        
        self.assertEquals(response.status_code, 404)

    def test_unlogined_profile_view_GET(self):
        url = reverse('profile', args=(self.user.slug,))
        response = self.client.get(url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/profile_page.html')
        
    def test_logined_settings_view_GET(self):
        self.client.force_login(self.user)
        url = reverse('profile-settings-information', args=(self.user.id,))
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/settings/information.html')
        
        url = reverse('profile-settings-security', args=(self.user.id,))
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/settings/security.html')
        
        url = reverse('profile-settings-site', args=(self.user.id,))
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/settings/site.html')
        
        url = reverse('profile-settings-notifications', args=(self.user.id,))
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/settings/notifications.html')
        
    def test_not_found_settings_view_GET(self):
        url = reverse('profile-settings-information', args=(123123,))
        response = self.client.get(url)
        self.assertEquals(response.status_code, 302)
        
        url = reverse('profile-settings-security', args=(123123,))
        response = self.client.get(url)
        self.assertEquals(response.status_code, 302)
        
        url = reverse('profile-settings-site', args=(123123,))
        response = self.client.get(url)
        self.assertEquals(response.status_code, 302)
        
        url = reverse('profile-settings-notifications', args=(123123,))
        response = self.client.get(url)
        self.assertEquals(response.status_code, 302)
        
    def test_unlogined_settings_view_GET(self):
        url = reverse('profile-settings-information', args=(self.user.id,))
        response = self.client.get(url)
        self.assertEquals(response.status_code, 302)
        
        url = reverse('profile-settings-security', args=(self.user.id,))
        response = self.client.get(url)
        self.assertEquals(response.status_code, 302)
        
        url = reverse('profile-settings-site', args=(self.user.id,))
        response = self.client.get(url)
        self.assertEquals(response.status_code, 302)

        url = reverse('profile-settings-notifications', args=(self.user.id,))
        response = self.client.get(url)
        self.assertEquals(response.status_code, 302)
    
    def test_post_information_settings_view(self):
        self.client.force_login(self.user)
        url = reverse('profile-settings-information', kwargs={'user_id': self.user.id})

        # Test POST update
        response = self.client.post(url, {
            'username': 'updateduser',
            'email': 'updateduser@example.com',
            'avatar': self.user.avatar
        })
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, 'updateduser')
        self.assertEqual(self.user.email, 'updateduser@example.com')

    def test_post_site_settings_view(self):
        self.client.force_login(self.user)
        url = reverse('profile-settings-site', kwargs={'user_id': self.user.id})

        # Test POST update
        response = self.client.post(url, {
            'description': 'Updated description',
            'age': 30
        })
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.description, 'Updated description')
        self.assertEqual(self.profile.age, 30)

    def test_post_notifications_settings_view(self):
        self.client.force_login(self.user)
        url = reverse('profile-settings-notifications', kwargs={'user_id': self.user.id})

        # Test POST update
        response = self.client.post(url, {
            'notificate_planning': False,
            'notificate_reading': False,
            'notificate_read': True,
            'notificate_abandonded': False
        })
        self.profile.refresh_from_db()
        self.assertFalse(self.profile.notificate_planning)
        self.assertFalse(self.profile.notificate_reading)
        self.assertTrue(self.profile.notificate_read)
        self.assertFalse(self.profile.notificate_abandonded)

    def test_post_security_settings_view(self):
        self.client.force_login(self.user)
        url = reverse('profile-settings-security', kwargs={'user_id': self.user.id})

        # Test POST change password
        response = self.client.post(url, {
            'old_password': 'username123',
            'new_password1': 'newtestpassword123',
            'new_password2': 'newtestpassword123'
        })
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('newtestpassword123'))
        
