"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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

from django.urls import path
from .views import login_view
from .views import register_user
from .views import get_goods
from .views import check_user_preferences
from .views import save_user_preferences
from .views import fetchAppImages
# from .views import search
from .views import get_category
from .views import send_sms_code
from .views import starGood
from .views import notStarGood
from .views import fetchPriceData

urlpatterns = [
    path('api/login/', login_view, name='login_view'),  # 新增登录接口
    path('api/register/', register_user, name='register_user'),
    path('api/get-goods/', get_goods, name='get_goods'),
    path('api/check-preferences/', check_user_preferences, name='check_user_preferences'),
    path('api/save-preferences/', save_user_preferences, name='save_user_preferences'),
    path('api/get-app-images/', fetchAppImages, name='fetch_app_images'),
    path('api/starGood/', starGood, name='starGood'),
    path('api/notStarGood/', notStarGood, name='notStarGood'),
    # path('api/search/', search, name='search'),
    path('api/get_category/', get_category, name='get_category'),
    path('api/send_sms_code/', send_sms_code, name='send_sms_code'),
    path('api/fetchPriceData/', fetchPriceData, name='fetchPriceData'),
]

