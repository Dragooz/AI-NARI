"""ainari URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path, include
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('paddy_area_detail/<str:paddy_area_name>/', views.paddy_area_detail, name='paddy_area_detail'),
    path('ajax/take_action/', views.take_action, name='take_action'),
    path('create_info', views.create_info, name='create_info'),
    path('test_image', views.test_image, name='test_image'),
    path('test_info', views.test_info, name='test_info'),
    # path('test/', views.test, name='test')
]
