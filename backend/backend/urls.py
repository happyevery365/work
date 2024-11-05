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
from .views import get_data, login_view
from .views import register_user
from .views import search_product

urlpatterns = [
    path('api/data/', get_data, name='get_data'),
    path('api/login/', login_view, name='login_view'),  # 新增登录接口
    path('api/register/', register_user, name='register_user'),
    path('api/search_product/', search_product, name='search_product'),
]

