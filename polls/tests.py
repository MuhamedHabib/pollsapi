from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework.test import APIRequestFactory
from polls import apiviews
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

class TestPoll(APITestCase):
    def setUp(self):
        #.3 Using APIClient
        #self.factory = APIRequestFactory()
        self.client=APIClient()

        self.view = apiviews.PollViewSet.as_view({'get': 'list'})
        self.uri = '/polls/'
        '''
        8.2 Testing APIs with authentication
        To test apis with authentication, a test user needs to be created so that we can make requests in context of that user.
        Let’s create a test user. Change your tests to
        '''
        self.user = self.setup_user()
        self.token = Token.objects.create(user=self.user)
        self.token.save()

    @staticmethod
    def setup_user():
        User = get_user_model()

        return User.objects.create_user(
            'test',
            email='testuser@test.com',
            password='test'
    )

    '''
    #uncomment this when you would using APIRequestFactory test method above
    def test_list(self):
        request = self.factory.get(self.uri,
            HTTP_AUTHORIZATION='Token {}'.format(self.token.key))
        request.user = self.user
        response = self.view(request)
        self.assertEqual(response.status_code, 200,
                         'Expected Response Code 200, received {0} instead.'
                         .format(response.status_code))
    '''
    def test_list2(self):
        self.client.login(username="test", password="test")
        response = self.client.get(self.uri)
        self.assertEqual(response.status_code, 200,
                         'Expected Response Code 200, received {0} instead.'
                         .format(response.status_code))

    def test_create(self):
        self.client.login(username="test", password="test")

        params = {
             "question": "How are you?",
             "created_by": 1
             }
        response = self.client.post(self.uri, params)
        self.assertEqual(response.status_code, 201,
                     'Expected Response Code 201, received {0} instead.'
                     .format(response.status_code))


'''
8.3 Using APIClient
The same test can be written using APIClient. It has get, .post and family. Unlike creating requests first, with
APIClient you can GET or POST to a url directly and get a response.
Add a test like this:
'''