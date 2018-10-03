from django.urls import path, include
from django.conf.urls import url
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('users', views.UserViewSet)
router.register('regions/provinsi', views.ProvinsiViewSet)
router.register('regions/kabupaten', views.KabupatenViewSet)
router.register('taxonomy', views.TaxonomyViewSet)
router.register('images', views.ImageViewSet)
router.register('ads', views.AdViewSet)

api_urlpatterns = [
    path('register/', views.RegisterView.as_view()),
    path('password/email/', views.PasswordEmailView.as_view()),
    path('password/reset/', views.PasswordResetView.as_view()),
    path('', include(router.urls)),
]

urlpatterns = [
    path('api/', include(api_urlpatterns)),
    url(r'.*', views.index),
]