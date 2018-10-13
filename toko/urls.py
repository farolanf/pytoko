from django.urls import path, include
from django.conf.urls import url
from django.shortcuts import render
from rest_framework.routers import DefaultRouter
from . import views

def template(name, context=None):
    def _render(request):
        return render(request, name, context=context)
    return _render

app_name = 'toko'

router = DefaultRouter()
router.register('users', views.UserViewSet)
router.register('regions/provinsi', views.ProvinsiViewSet)
router.register('regions/kabupaten', views.KabupatenViewSet)
router.register('taxonomy', views.TaxonomyViewSet)
router.register('images', views.AdImageViewSet)
router.register('ads', views.AdViewSet)

api_urlpatterns = [
    path('register/', views.RegisterView.as_view()),
    path('password/email/', views.PasswordEmailView.as_view()),
    path('password/reset/', views.PasswordResetView.as_view()),
    path('', include(router.urls)),
]

urlpatterns = [
    path('api/', include(api_urlpatterns)),
    url(r'^$', template('toko/front.html'), name='front'),

    path('accounts/login/', views.LoginView.as_view(), name='login'),
    path('accounts/logout/', views.logout_view, name='logout'),
    path('accounts/register/', views.RegisterView.as_view(), name='register'),
    path('accounts/register-success/', template('toko/account/register-success.html'), name='register-success'),

    path('accounts/ads/', views.MyAds.as_view(), name='my-ads'),
    path('accounts/ads/<int:pk>/', views.AdEdit.as_view(), name='ad-edit'),
]