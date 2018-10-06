import sys
from enum import Enum
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED, HTTP_403_FORBIDDEN, HTTP_204_NO_CONTENT
from .base import TestCase
from .utils.user import User

actions = {
    """
    as_param: If True, action will be added to the base url.
        Eg. /api/ads/{action}/
    """
    'can': {
        'list': {
            'method': 'get',
            'detail': False,
            'expected_status': HTTP_200_OK,
        },
        'view': {
            'method': 'get',
            'detail': True,
            'expected_status': HTTP_200_OK,
        },
        'create': {
            'method': 'post',
            'detail': False,
            'expected_status': HTTP_400_BAD_REQUEST,
        },
        'update': {
            'method': 'put',
            'detail': True,
            'expected_status': HTTP_400_BAD_REQUEST,
        },
        'delete': {
            'method': 'delete',
            'detail': True,
            'expected_status': HTTP_204_NO_CONTENT,
        },
        'my': {
            'method': 'get',
            'detail': False,
            'as_param': True,
            'expected_status': HTTP_200_OK,
        },
    },
    'cannot': {
        'list': {
            'method': 'get',
            'detail': False,
        },
        'view': {
            'method': 'get',
            'detail': True,
        },
        'create': {
            'method': 'post',
            'detail': False,
        },
        'update': {
            'method': 'put',
            'detail': True,
        },
        'delete': {
            'method': 'delete',
            'detail': True,
        },
        'my': {
            'method': 'get',
            'detail': False,
            'as_param': True,
        },
    }
}

def can_action(action, method, detail, expected_status, as_param=False):

    def test_method(self):
        base_url = self.detail_url if detail else self.base_url
        url = '%s%s/' % (base_url, action) if as_param else base_url
        response = getattr(self.client, method)(url)
        self.assertEqual(response.status_code, expected_status)

    return test_method

def cannot_action(action, method, detail, as_param=False):

    def test_method(self):
        base_url = self.detail_url if detail else self.base_url
        url = '%s%s/' % (base_url, action) if as_param else base_url
        expected_status = HTTP_403_FORBIDDEN if self.login else HTTP_401_UNAUTHORIZED
        response = getattr(self.client, method)(url)
        self.assertEqual(response.status_code, expected_status)

    return test_method

def inject_test_methods(cls):
    """
    Create test methods on the derived class based on permission config.
    
    This is so test error reporting points to the derived class.
    """
    for action in cls.can:
        kwargs = actions['can'][action]
        kwargs['action'] = action
        setattr(cls, 'test_can_%s' % action, can_action(**kwargs))

    for action in cls.cannot:
        kwargs = actions['cannot'][action]
        kwargs['action'] = action
        setattr(cls, 'test_cannot_%s' % action, cannot_action(**kwargs))

class PermissionMixin(object):

    def __init__(self, *args, **kwargs):

        # assume base_url ends with slash
        self.detail_url = '%s%s/' % (self.base_url, self.detail_pk)

        super().__init__(*args, **kwargs)

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

# anonymous user access to post ads
class AdsPublicPermissionTestBase(PermissionTestBase):
    can = ('list', 'view')
    cannot = ('create', 'update', 'delete', 'my')

# authenticated user access to own post ads
class AdsOwnerPermissionTestBase(PermissionTestBase):
    can = ('list', 'view', 'create', 'update', 'my')
    cannot = ('delete',)

# authenticated user access to other's post ads
class AdsOtherPermissionTestBase(PermissionTestBase):
    can = ('list', 'view', 'create', 'my')
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

class AdPublicPermissionTest(AdsPublicPermissionTestBase):
    base_url = '/api/ads/'
    fixtures = ['users.json', 'taxonomy.json', 'regions.json', 'ads.json']

class AdOwnerPermissionTest(AdsOwnerPermissionTestBase):
    base_url = '/api/ads/'
    fixtures = ['users.json', 'taxonomy.json', 'regions.json', 'ads.json']
    role = Role.OWNER

class AdOtherPermissionTest(AdsOtherPermissionTestBase):
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