from .models import UserInfo
from django import forms
from django.core.validators import RegexValidator


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
