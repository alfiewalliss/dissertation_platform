from django.test import TestCase
from .models import Tag
from django.contrib.auth.models import User
from django.contrib.auth import authenticate


class UserTest(TestCase):
    testUsers = [User.objects.create(username="alfie"), User.objects.create(username="testuser")]
    def test_user(self):
        users = User.objects.all()
        print(users)
        first = authenticate(username="alfie")
        second = authenticate(username="testuser")
        self.assertEqual(first.email, "alfie.walliss@gmail.com")
        self.assertEqual(second.email, "aw840@exeter.ac.uk")

# Test the tag model 
class TagTestCase(TestCase):
    def setUp(self):
        tag1 = Tag.objects.create(tags="First tag")
        tag2 = Tag.objects.create(tags="Second tag")
        tag1.followers.set(UserTest.setUp())
        tag2.followers.set(UserTest.setUp())


    def test_tag(self):
        """Animals that can speak are correctly identified"""
        first = Tag.objects.get(tags="First tag")
        second = Tag.objects.get(tags="Second tag")
        self.assertEqual(first.__str__(), 'First tag')
        self.assertEqual(second.__str__(), 'Second tag')