from django.urls import path
from . import views


app_name = "mainapp"

# 主url中设置了namespace，反向解析时应为"mainapp: register"
urlpatterns = [
    # 试用腾讯云短信
    path('sms/', views.send_massage, name='sms'),
    # 用户注册
    path('register/', views.register, name='register'),

]
