from django.urls import path, include
from django.conf.urls import url
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('users', views.UserViewSet)

api_urlpatterns = [
    path('', include(router.urls)),
]

urlpatterns = [
    path('api/', include(api_urlpatterns)),
    url(r'.*', views.index),
]