from django.urls import path
from .views import account, project


app_name = "mainapp"

# 主url中设置了namespace，反向解析时应为"mainapp: register"
urlpatterns = [
    # 首页
    path('index/', account.home, name='index'),
    # 试用腾讯云短信
    path('sms/', account.send_massage, name='sms'),
    # 用户注册
    path('register/', account.register, name='register'),
    # 用户短信登录
    path('login/sms/', account.login_sms, name='login_sms'),
    # 用户名或手机登录
    path('login/', account.login, name='login'),
    # 图片验证码获取
    path('image_code/', account.image_code, name='image_code'),
    # 用户退出
    path('logout/', account.logout, name='logout'),

    # 项目管理
    path('project/list/', project.project_list, name='project_list'),
]
