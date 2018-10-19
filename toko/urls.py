from django.urls import path, include
from django.conf.urls import url
from django.shortcuts import render
from rest_framework.routers import DefaultRouter
from . import views
from .routers import AppRouter

def template(name, context=None):
    def _render(request):
        return render(request, name, context=context)
    return _render

app_name = 'toko'

api_router = DefaultRouter()
api_router.register('users', views.AdminUserViewSet, base_name='admin-user')
api_router.register('files', views.AdminFileViewSet, base_name='admin-file')
api_router.register('provinsi', views.AdminProvinsiViewSet, base_name='admin-provinsi')
api_router.register('kabupaten', views.AdminKabupatenViewSet, base_name='admin-kabupaten')
api_router.register('taxonomy', views.AdminTaxonomyViewSet, base_name='admin-taxonomy')
api_router.register('adimages', views.AdminAdImageViewSet, base_name='admin-ad-image')
api_router.register('ads', views.AdminAdViewSet, base_name='admin-ad')

router = AppRouter()
router.register('ads', views.AdViewSet)
router.register('kabupaten', views.KabupatenViewSet)
router.register('files', views.FileViewSet)

urlpatterns = [
    url(r'^$', template('toko/front.html'), name='front'),

    path('accounts/', template('toko/account/home.html'), name='home'),

    path('accounts/login/', views.LoginView.as_view(), name='login'),
    path('accounts/logout/', views.logout_view, name='logout'),
    path('accounts/register/', views.RegisterView.as_view(), name='register'),

    path('accounts/register-success/', template('toko/account/register-success.html'), name='register-success'),

    path('accounts/forgot-password/', views.ForgotPasswordView.as_view(), name='forgot-password'),

    path('accounts/forgot-password-success/', template('toko/account/forgot-password-success.html'), name='forgot-password-success'),

    path('accounts/reset-password/', views.ResetPasswordView.as_view(), name='reset-password'),
    path('accounts/reset-password/<token>/', views.ResetPasswordView.as_view(), name='reset-password'),

    path('api/', include(api_router.urls)),
    path('', include(router.urls)),
]