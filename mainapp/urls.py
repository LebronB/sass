from django.urls import path
from . import views


app_name = "mainapp"

# 主url中设置了namespace，反向解析时应为"mainapp: register"
urlpatterns = [
    # 首页
    path('index/', views.home, name='index'),
    # 试用腾讯云短信
    path('sms/', views.send_massage, name='sms'),
    # 用户注册
    path('register/', views.register, name='register'),
    # 用户短信登录
    path('login/sms/', views.login_sms, name='login_sms'),
    # 用户名或手机登录
    path('login/', views.login, name='login'),
    # 图片验证码获取
    path('image_code/', views.image_code, name='image_code'),
    # 用户退出
    path('logout/', views.logout, name='logout'),
]
