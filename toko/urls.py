from django.urls import path, include
from django.conf.urls import url
from django.shortcuts import render
from rest_framework.routers import DefaultRouter, SimpleRouter
from . import views

def template(name, context=None):
    def _render(request):
        return render(request, name, context=context)
    return _render

app_name = 'toko'

api_router = DefaultRouter()
api_router.register('users', views.UserViewSet)
api_router.register('provinsi', views.ProvinsiViewSet)
api_router.register('kabupaten', views.KabupatenViewSet)
api_router.register('taxonomy', views.TaxonomyViewSet)
api_router.register('images', views.AdImageViewSet)
api_router.register('ads', views.AdViewSet, base_name='api-ads')

api_urlpatterns = [
    path('register/', views.RegisterView.as_view()),
    path('password/email/', views.PasswordEmailView.as_view()),
    path('password/reset/', views.PasswordResetView.as_view()),
    path('', include(api_router.urls)),
]

router = SimpleRouter()
router.register('ads', views.UserAdViewSet)

urlpatterns = [
    url(r'^$', template('toko/front.html'), name='front'),

    path('accounts/login/', views.LoginView.as_view(), name='login'),
    path('accounts/logout/', views.logout_view, name='logout'),
    path('accounts/register/', views.RegisterView.as_view(), name='register'),
    path('accounts/register-success/', template('toko/account/register-success.html'), name='register-success'),

    path('api/', include(api_urlpatterns)),
    path('', include(router.urls)),
]