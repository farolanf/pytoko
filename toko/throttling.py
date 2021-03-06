from rest_framework.throttling import AnonRateThrottle

class PasswordEmailThrottle(AnonRateThrottle):
    scope = 'password-email'

class SearchThrottle(AnonRateThrottle):
    scope = 'search'