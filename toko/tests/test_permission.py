import sys
from enum import Enum
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED, HTTP_403_FORBIDDEN, HTTP_204_NO_CONTENT
from .base import TestCase
from .utils.user import User
from .utils.permission import inject_test_methods

class PermissionMixin(object):

    def __init__(self, *args, **kwargs):

        # assume base_url ends with slash
        self.detail_url = '%s%s/' % (self.base_url, self.detail_pk)

        super().__init__(*args, **kwargs)

    """ can """

    def can_list(self):
        response = self.client.get(self.base_url)
        self.assertEqual(response.status_code, HTTP_200_OK)

    def can_view(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, HTTP_200_OK)

    def can_create(self):
        """
        Expect a bad request status when creating with no data.

        If it made it this far then auth and authorization has succeeded.
        """
        response = self.client.post(self.base_url)
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)

    def can_update(self):
        """
        Expect a not found status when updating with no data.

        If it made it this far then auth and authorization has succeeded.
        """
        response = self.client.put(self.detail_url)
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)

    def can_delete(self):
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, HTTP_204_NO_CONTENT)

    """ cannot """

    def cannot_list(self):
        expected_status = HTTP_403_FORBIDDEN if self.login else HTTP_401_UNAUTHORIZED
        response = self.client.get(self.base_url)
        self.assertEqual(response.status_code, expected_status)

    def cannot_view(self):
        expected_status = HTTP_403_FORBIDDEN if self.login else HTTP_401_UNAUTHORIZED
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, expected_status)

    def cannot_create(self):
        expected_status = HTTP_403_FORBIDDEN if self.login else HTTP_401_UNAUTHORIZED
        response = self.client.post(self.base_url)
        self.assertEqual(response.status_code, expected_status)

    def cannot_update(self):
        expected_status = HTTP_403_FORBIDDEN if self.login else HTTP_401_UNAUTHORIZED
        response = self.client.put(self.detail_url)
        self.assertEqual(response.status_code, expected_status)

    def cannot_delete(self):
        expected_status = HTTP_403_FORBIDDEN if self.login else HTTP_401_UNAUTHORIZED
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, expected_status)

class Role(Enum):
    ANON = 1
    OWNER = 2
    OTHER = 3

class PermissionTestBase(PermissionMixin, TestCase):
    base_url = '/api/.../'
    fixtures = ['users.json']

    # user role
    role = Role.ANON

    # the object to be inspected
    detail_pk = 1

    # permissions - the list of actions (list, view, create, update, delete)    
    can = ()
    cannot = ()

    def setUp(self):
        super().setUp()

        self.login = self.role != Role.ANON

        if self.role != Role.ANON:
            pk = 1 if self.role == Role.OWNER else 2
            
            password = 'somepassword22'

            user = User.objects.get(pk=pk)
            user.set_password(password)
            user.save()
            
            self.client.login(email=user.email, password=password)

""" Permission Configs """

# anonymous user access to a resource
class BrowsePublicPermissionTestBase(PermissionTestBase):
    can = ('list', 'view')
    cannot = ('create', 'update', 'delete')

# authenticated user access to a resource
class BrowseAuthPermissionTestBase(BrowsePublicPermissionTestBase):
    pass

# anonymous user access to users
class UserPublicPermissionTestBase(PermissionTestBase):
    can = ('view',)
    cannot = ('list', 'create', 'update', 'delete')

# authenticated user access to self
class UserSelfPermissionTestBase(PermissionTestBase):
    can = ('view', 'update')
    cannot = ('list', 'create', 'delete')

# authenticated user access to other users
class UserOtherPermissionTestBase(UserPublicPermissionTestBase):
    pass

# anonymous user access to post resource
class PostPublicPermissionTestBase(BrowsePublicPermissionTestBase):
    pass

# authenticated user access to own post resource
class PostOwnerPermissionTestBase(PermissionTestBase):
    can = ('list', 'view', 'create', 'update')
    cannot = ('delete',)

# authenticated user access to other's post resource
class PostOtherPermissionTestBase(PermissionTestBase):
    can = ('list', 'view', 'create')
    cannot = ('update', 'delete')

""" TESTS """

class TaxonomyPublicPermissionTest(BrowsePublicPermissionTestBase):
    base_url = '/api/taxonomy/'
    fixtures = ['users.json', 'taxonomy.json']
    detail_pk = 14

class TaxonomyAuthPermissionTest(BrowseAuthPermissionTestBase):
    base_url = '/api/taxonomy/'
    fixtures = ['users.json', 'taxonomy.json']
    detail_pk = 14
    role = Role.OWNER

class UserPublicPermissionTest(UserPublicPermissionTestBase):
    base_url = '/api/users/'

class UserSelfPermissionTest(UserSelfPermissionTestBase):
    base_url = '/api/users/'
    role = Role.OWNER

class UserOtherPermissionTest(UserOtherPermissionTestBase):
    base_url = '/api/users/'
    role = Role.OTHER

class AdPublicPermissionTest(PostPublicPermissionTestBase):
    base_url = '/api/ads/'
    fixtures = ['users.json', 'taxonomy.json', 'regions.json', 'ads.json']

class AdOwnerPermissionTest(PostOwnerPermissionTestBase):
    base_url = '/api/ads/'
    fixtures = ['users.json', 'taxonomy.json', 'regions.json', 'ads.json']
    role = Role.OWNER

class AdOtherPermissionTest(PostOtherPermissionTestBase):
    base_url = '/api/ads/'
    fixtures = ['users.json', 'taxonomy.json', 'regions.json', 'ads.json']
    role = Role.OTHER

inject_test_methods(TaxonomyPublicPermissionTest)
inject_test_methods(TaxonomyAuthPermissionTest)

inject_test_methods(UserPublicPermissionTest)
inject_test_methods(UserSelfPermissionTest)
inject_test_methods(UserOtherPermissionTest)

inject_test_methods(AdPublicPermissionTest)
inject_test_methods(AdOwnerPermissionTest)
inject_test_methods(AdOtherPermissionTest)