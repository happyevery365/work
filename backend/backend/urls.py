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
from .views import append_user_preferences
from .views import fetchAppImages
from .views import search
from .views import get_category
from .views import send_sms_code
from .views import fetchPriceData
from .views import price_compare
from .views import change_password
from .views import change_preferences
from .views import searchIfStarred
from .views import star_goods
from .views import unstar_goods
from .views import get_preferrence_goods
from .views import get_unseen_goods_count
from .views import newChangedGoods
from .views import oldChangedGoods
from .views import check_user_not_preferences
from .views import check_user_preference_category
from .views import delete_user_preferences
from .views import save_cookie

urlpatterns = [
    path('api/login/', login_view, name='login_view'),  # 新增登录接口
    path('api/register/', register_user, name='register_user'),
    path('api/get-goods/', get_goods, name='get_goods'),
    path('api/get-preferrencegoods/', get_preferrence_goods, name='get_preferrence_goods'),
    path('api/check-preferences/', check_user_preferences, name='check_user_preferences'),
    path('api/check_user_preference_category/', check_user_preference_category, name='check_user_preference_category'),
    path('api/check_user_not_preferences/', check_user_not_preferences, name='check_user_not_preferences'),
    path('api/save-preferences/', save_user_preferences, name='save_user_preferences'),
    path('api/delete_user_preferences/', delete_user_preferences, name='delete_user_preferences'),
    path('api/append-preferences/', append_user_preferences, name='append_user_preferences'),
    path('api/change-preferences/', change_preferences, name='change_preferences'),
    path('api/get-app-images/', fetchAppImages, name='fetch_app_images'),
    path('api/search/', search, name='search'),
    path('api/get_category/', get_category, name='get_category'),
    path('api/send_sms_code/', send_sms_code, name='send_sms_code'),
    path('api/fetchPriceData/', fetchPriceData, name='fetchPriceData'),
    path('api/price_compare/', price_compare, name='price_compare'),
    path('api/change_password/', change_password, name='change_password'),
    path('api/searchIfStarred/', searchIfStarred, name='searchIfStarred'),
    path('api/star_goods/', star_goods, name='star_goods'),
    path('api/unstar_goods/', unstar_goods, name='unstar_goods'),
    path('api/get-unseen-goods-count/', get_unseen_goods_count, name='get_unseen_goods_count'),
    path('api/newChangedGoods/', newChangedGoods, name='newChangedGoods'),
    path('api/oldChangedGoods/', oldChangedGoods, name='oldChangedGoods'),
    path('api/save_cookie/', save_cookie, name='save_cookie'),
]

