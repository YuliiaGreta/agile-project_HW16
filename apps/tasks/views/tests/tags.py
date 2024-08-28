from django.test import TestCase

class TagsTestCase(TestCase):
    def test_home_page(self):
        response = self.client.get('/')
        self.assertContains(response, "Welcome to my site!")