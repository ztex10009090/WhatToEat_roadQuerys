"""WhatToEat_roadQuerys URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from users import views as views_users
from roadQuerys import views as views_roadQuerys
from myFavourite import views as views_myFavourite

urlpatterns = [
    path('admin/', admin.site.urls),

    url(r'^home', views_users.index, name='index'),
    url(r'^Picture/Create', views_users.createPicture, name='users_create'),

    url(r'^User/Login', views_users.login, name='users_login'),
    url(r'^User/ThreePartLogin', views_users.threePartLogin, name='users_threePartLogin'),

    url(r'^User/SignUp', views_users.signUp, name='users_signUp'),

    url(r'^User/UpdatePassword', views_users.updatePassword, name='users_updatePassword'),
    url(r'^User/ForgetPassword', views_users.forgetPassword, name='users_forgetPassword'),
    url(r'^User/VerifyCode', views_users.verifyCode, name='users_verifyCode'),
    url(r'^User/ResetPassword', views_users.resetPassword, name='users_resetPassword'),
    url(r'^User/UpdatePicture', views_users.updatePicture, name='users_updatePicture'),

    url(r'^RoadQuery/Create', views_roadQuerys.createRoadQuery, name='roadQuerys_createRoadQuery'),
    url(r'^RoadQuery/GetRoadQuery', views_roadQuerys.getRoadQuery, name='roadQuerys_getRoadQuery'),
    url(r'^RoadQuery/GetClassify', views_roadQuerys.getClassify, name='roadQuerys_getClassify'),
    url(r'^RoadQuery/GetList', views_roadQuerys.getRoadQueryList, name='roadQuerys_getRoadQueryList'),
    url(r'^RoadQuery/GetSearch', views_roadQuerys.getSearch, name='roadQuerys_getSearch'),
    url(r'^RoadQuery/GetAdvancedSearch', views_roadQuerys.getAdvancedSearch, name='roadQuerys_getAdvancedSearch'),

    url(r'^MyFavourite', views_myFavourite.get_myfavourite, name='myfavorite'),
]+ static('/images/', document_root=settings.IMAGE_ROOT)
