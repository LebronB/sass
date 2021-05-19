from .models import UserInfo
from django import forms
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.conf import settings
import random
from utils.tencent.sms import send_sms_single
from django_redis import get_redis_connection


class RegisterModelForm(forms.ModelForm):
    mobile_phone = forms.CharField(
        label='手机号码',
        validators=[RegexValidator(r'^(1[3|4|5|6|7|8|9])\d{9}$', '手机号码格式错误')]
    )
    password = forms.CharField(label='密码')
    confirm_password = forms.CharField(label='确认密码')
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = '请输入%s' % field.label


class SendMsgForm(forms.Form):
    # 使用regex验证格式
    mobile_phone = forms.CharField(label="手机号", validators=[RegexValidator(r'^(1[3|4|5|6|7|8|9])\d{9}$', '手机号码格式错误')])

    # 将request传进来，就在forms中使用request的信息
    def __init__(self, request, *args, **kwargs):
        self.request = request
        super().__init__(*args, **kwargs)

    # 校验 1. 模板是否正确 2. 手机号是否已注册
    def clean_mobile_phone(self):
        mobile_phone = self.cleaned_data['mobile_phone']

        tpl = self.request.GET.get('tpl')
        template_id = settings.TENCENT_SMS_TEMPLATE.get(tpl)
        if not template_id:
            raise ValidationError("短信模板错误")

        # 校验数据库中是否存在该手机号
        exists = UserInfo.objects.filter(mobile_phone=mobile_phone).exists()
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