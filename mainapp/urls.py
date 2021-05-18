from django.urls import path
from . import views


app_name = "mainapp"

urlpatterns = [
    # 试用腾讯云短信
    path('sms/', views.send_massage, name='sms'),
    # 用户注册
    path('register/', views.register, name='register'),

]
