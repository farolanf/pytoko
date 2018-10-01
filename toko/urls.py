from django.urls import path, include
from django.conf.urls import url
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('users', views.UserViewSet)

api_urlpatterns = [
    path('password/email/', views.PasswordEmailView.as_view()),
    path('password/reset/', views.PasswordResetView.as_view()),
    path('', include(router.urls)),
]

urlpatterns = [
    path('api/', include(api_urlpatterns)),
    url(r'.*', views.index),
]