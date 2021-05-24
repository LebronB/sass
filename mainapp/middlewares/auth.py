from django.utils.deprecation import MiddlewareMixin
from mainapp.models import UserInfo


class AuthMiddleware(MiddlewareMixin):
    def process_request(self, request):
        """如果用户已登录，，则在request中赋值"""
        user_id = request.session.get('user_id', 0)
        user_object = UserInfo.objects.filter(id=user_id).first()
        request.tracer = user_object
