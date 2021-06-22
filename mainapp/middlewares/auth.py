from datetime import datetime

from django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin
from mainapp.models import UserInfo, Project, ProjectUser
from django.conf import settings
from mainapp.models import Transaction, PricePolicy


class Tracer:
    def __init__(self):
        """用于封装返回给view的tracer对象"""
        self.user = None
        self.price_policy = None
        self.project = None


class AuthMiddleware(MiddlewareMixin):
    def process_request(self, request):
        """如果用户已登录，，则在request中赋值"""

        request.tracer = Tracer()

        user_id = request.session.get('user_id', 0)
        user_object = UserInfo.objects.filter(id=user_id).first()
        request.tracer.user = user_object

        # 白名单：没有登录也可以访问的页面
        """
        获取用户访问的url，检查是否在白名单当中，若在白名单，return表示中间件通过
        """
        if request.path_info in settings.WHITE_REGEX_URL_LIST:
            return

        if not request.tracer.user:
            return redirect('mainapp:login')

        # 获取该用户最后一次的交易记录
        trans = Transaction.objects.filter(user=user_object, status=2).order_by('-id').first()
        # 判断是否已经过期
        current_datetime = datetime.now()
        if trans.end_datetime and current_datetime > trans.end_datetime:
            # 最后一次购买已过期，获取免费额度的记录
            trans = Transaction.objects.filter(user=user_object, status=2, price_policy__category=1).first()
        request.tracer.price_policy = trans.price_policy

        # _object = Transaction.objects.filter(user=user_object, status=2).order_by('-id').first()
        # if not _object:
        #     # 没有购买
        #     request.price_policy = PricePolicy.objects.filter(category=1, title="个人免费版").first()
        # else:
        #     current_datetime = datetime.now()
        #     if _object.end_datetime and current_datetime > _object.end_datetime:
        #         # 最后一次购买已过期，获取免费额度的记录
        #         request.price_policy = Transaction.objects.filter(user=user_object, status=2, price_policy__category=1).first()
        #     else:
        #         request.price_policy = _object.price_policy

    def process_view(self, request, view, args, kwargs):
        if not request.path_info.startswith('/manage/'):
            return
        # 判断是否是自己的项目
        project_id = kwargs.get('project_id')
        project_obj = Project.objects.filter(creator=request.tracer.user, id=project_id).first()
        if project_obj:
            request.tracer.project = project_obj
            return
        # 不是自己创建的，判断是否是自己参与的
        project_obj = ProjectUser.objects.filter(user=request.tracer.user, project_id=project_id).first()
        if project_obj:
            request.tracer.project = project_obj.project
            return

        # 都不属于
        return redirect('mainapp:project_list')