from django.urls import path, include
from .views import account, project, manage, wiki


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

    # 项目列表
    path('project/list/', project.project_list, name='project_list'),
    # 星标项目
    path('project/star/<str:project_type>/<int:project_id>/', project.project_star, name='project_star'),
    # 取消星标
    path('project/unstar/<str:project_type>/<int:project_id>/', project.project_unstar, name='project_unstar'),

    # 项目管理
    path('manage/<int:project_id>/', include([
        path('dashboard/', manage.dashboard, name='dashboard'),
        path('issues/', manage.issues, name='issues'),
        path('statistics/', manage.statistics, name='statistics'),

        path('wiki/', wiki.wiki, name='wiki'),
        path('wiki/add/', wiki.wiki_add, name='wiki_add'),
        path('wiki/catalog/', wiki.wiki_catalog, name='wiki_catalog'),
        path('wiki/delete/<int:wiki_id>/', wiki.wiki_delete, name='wiki_delete'),
        path('wiki/edit/<int:wiki_id>/', wiki.wiki_edit, name='wiki_edit'),

        path('files/', manage.files, name='files'),
        path('settings/', manage.settings, name='settings'),
    ])),
]
