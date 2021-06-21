import random

from django import forms
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django_redis import get_redis_connection

from utils.encrypt import md5
from utils.tencent.sms import send_sms_single
from mainapp.models import UserInfo


# Bootstrap基类，用于给表单添加样式以及placeholder
class BootStrapForm(object):

    bootstrap_class_exclude = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            # 部分字段应用样式
            if name in self.bootstrap_class_exclude:
                continue
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = '请输入%s' % field.label


class RegisterModelForm(BootStrapForm, forms.ModelForm):
    password = forms.CharField(
        label='密码',
        min_length=8,
        max_length=16,
        error_messages={
            'min_length': '密码长度不能小于8个字符',
            'max_length': '密码长度不能大于16个字符'
        },
        widget=forms.PasswordInput()
    )
    confirm_password = forms.CharField(
        label='确认密码',
        min_length=8,
        max_length=16,
        error_messages={
            'min_length': '重复密码长度不能小于8个字符',
            'max_length': '重复密码长度不能大于16个字符'
        },
        widget=forms.PasswordInput()
    )
    mobile_phone = forms.CharField(
        label='手机号码',
        validators=[RegexValidator(r'^(1[3|4|5|6|7|8|9])\d{9}$', '手机号码格式错误')]
    )
    code = forms.CharField(label='验证码')

    class Meta:
        model = UserInfo
        fields = [
            'username',
            'email',
            'password',
            'confirm_password',
            'mobile_phone',
            'code'
        ]

    # 用户名钩子 不可重复
    def clean_username(self):
        username = self.cleaned_data['username']
        exists = UserInfo.objects.filter(username=username).exists()
        if exists:
            raise ValidationError("用户名已存在")

        return username

    # 邮箱钩子
    def clean_email(self):
        email = self.cleaned_data['email']
        exists = UserInfo.objects.filter(email=email).exists()
        if exists:
            raise ValidationError("邮箱已存在")

        return email

    # 密码钩子  对密码进行密文处理
    def clean_password(self):
        pwd = self.cleaned_data['password']
        return md5(pwd)

    # 重复密码钩子
    def clean_confirm_password(self):
        # 在清洗一个字段时，如果要拿另一个字段，使用get避免获取不到这个key的问题
        pwd = self.cleaned_data.get('password')
        confirm_pwd = md5(self.cleaned_data['confirm_password'])
        if pwd != confirm_pwd:
            raise ValidationError("两次密码不一致")

        return confirm_pwd

    # 手机号钩子
    def clean_mobile_phone(self):
        mobile_phone = self.cleaned_data['mobile_phone']
        exists = UserInfo.objects.filter(mobile_phone=mobile_phone).exists()
        if exists:
            raise ValidationError("手机号已注册")

        return mobile_phone

    # 验证码钩子
    # def clean_code(self):
    #     code = self.cleaned_data['code']
    #     mobile_phone = self.cleaned_data.get('mobile_phone')
    #
    #     # mobile_phone未验证通过，直接返回code
    #     if not mobile_phone:
    #         return code
    #     conn = get_redis_connection()
    #     redis_code = conn.get(mobile_phone)
    #     if not redis_code:
    #         raise ValidationError("验证码已失效或未发送，请重新发送")
    #
    #     redis_str_code = redis_code.decode('utf-8')
    #     if code.strip() != redis_str_code:
    #         raise ValidationError("验证码错误，请检查")
    #
    #     return code


class SendMsgForm(forms.Form):
    # 使用regex验证格式
    mobile_phone = forms.CharField(label="手机号", validators=[RegexValidator(r'^(1[3|4|5|6|7|8|9])\d{9}$', '手机号码格式错误')])

    # 将request传进来，就在forms中使用request的信息
    def __init__(self, request, *args, **kwargs):
        self.request = request
        super().__init__(*args, **kwargs)

    # 手机号钩子 1. 模板是否正确 2. 手机号是否已注册
    def clean_mobile_phone(self):
        mobile_phone = self.cleaned_data['mobile_phone']

        tpl = self.request.GET.get('tpl')
        template_id = settings.TENCENT_SMS_TEMPLATE.get(tpl)
        if not template_id:
            raise ValidationError("短信模板错误")

        # 校验数据库中是否存在该手机号
        exists = UserInfo.objects.filter(mobile_phone=mobile_phone).exists()
        if tpl == 'login':
            if not exists:
                raise ValidationError("手机号未注册")
        else:
            if exists:
                raise ValidationError("该号码已注册")

        # 发短信
        code = random.randrange(1000, 9999)
        ret = send_sms_single(mobile_phone, template_id, [code, ])
        if ret['result'] != 0:
            raise ValidationError("短信发送失败，{}".format(ret['result']))

        # 写入redis(django-redis)
        conn = get_redis_connection()
        conn.set(mobile_phone, code, ex=60)

        return mobile_phone


class LoginSmsForm(BootStrapForm, forms.Form):
    mobile_phone = forms.CharField(
        label='手机号码',
        validators=[RegexValidator(r'^(1[3|4|5|6|7|8|9])\d{9}$', '手机号码格式错误')]
    )
    code = forms.CharField(label='验证码')

    def clean_mobile_phone(self):
        mobile_phone = self.cleaned_data['mobile_phone']
        user_object = UserInfo.objects.filter(mobile_phone=mobile_phone).first()
        if not user_object:
            raise ValidationError("手机号未注册")
        return user_object

    def clean_code(self):
        user_object = self.cleaned_data.get('mobile_phone')
        code = self.cleaned_data['code']
        if not user_object:
            return code

        conn = get_redis_connection()
        redis_code = conn.get(user_object.mobile_phone)
        if not redis_code:
            raise ValidationError("验证码失效或未发送，请重试")

        redis_str_code = redis_code.decode('utf-8')
        if code.strip() != redis_str_code:
            raise ValidationError("验证码错误，请重新输入")

        return code


class LoginForm(BootStrapForm, forms.Form):
    username = forms.CharField(label="邮箱或手机号")
    # 上一次的输入值仍然保留在框中
    password = forms.CharField(label="密码", widget=forms.PasswordInput(render_value=True))
    code = forms.CharField(label="图片验证码")

    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request

    def clean_code(self):
        """图片验证码是否正确"""
        code = self.cleaned_data['code']
        # 取session中的验证码
        session_code = self.request.session.get('image_code')
        if not session_code:
            raise ValidationError("验证码已过期，请重新获取")
        # 比较验证码
        if code.strip().upper() != session_code.strip().upper():
            raise ValidationError("验证码输入错误")

        return code

    # 密码保存为密文
    def clean_password(self):
        """密码文本加密"""
        pwd = self.cleaned_data['password']
        return md5(pwd)