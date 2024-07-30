"""myproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from .views import *
# from .send import *
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',home,name='home'),
    path('log/',logcreation,name='logcreation'),
    path('shopify/',oauth_shopify,name='oauth_shopify'),
    path('commense_auth/',get_access_token,name='get_access_token'),
    path('base_url/',base_url,name='base_url'),
    path('home/',base2_url,name='home'),
    path('webhook',getwebhook,name='getwebhook'),
    path('yourjson/',YourAPIView.as_view(),name='yourjson'),
    # path('facebok/',facebookAouth,name='facebok'),
    # path('facebokredirect/',facebookAouthredirect,name='facebokredirect'),
]