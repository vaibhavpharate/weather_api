from django.urls import path, include
from .views import sample_page, create_client, admin_login,admin_home,add_site, premium,client_homepage,client_login, custom_403_view, client_login, basic,api_view

from .serializers import VBAViewSets
from rest_framework.routers import DefaultRouter
from .auth import CustomAuthToken

router = DefaultRouter()
router.register(r'tasks', VBAViewSets)


urlpatterns = [
    path("test",sample_page,name='sample_page'),
    path('create_client',create_client,name='create_client'),
    path("admin_home",admin_home, name="admin_home"),
    path('admin_login',admin_login,name='admin_login'),
    path('add_site',add_site,name='add_site'),
    path('premium',premium,name='premium'),
    path('basic',basic,name='basic'),
    path('client_login',client_login,name='client_login'),
    path('client',client_homepage,name='client_homepage'),
    path('client_login',client_login,name='client_login'),

    path('403',custom_403_view,name='403'),
    path('api_view',api_view,name='api_view')
    # path('get_token_data',CustomAuthToken.as_view())
    # path('', include(router.urls)),

]
