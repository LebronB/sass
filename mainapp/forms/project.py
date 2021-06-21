from django import forms
from django.core.exceptions import ValidationError

from .account import BootStrapForm
from mainapp.models import Project
from .widgets import ColorRadioSelect


class ProjectModelForm(BootStrapForm, forms.ModelForm):
    bootstrap_class_exclude = ['color']

    class Meta:
        model = Project
        fields = [
            'name',
            'color',
            'desc',
        ]
        # ModelForm中加入插件
        widgets = {
            'desc': forms.Textarea,
            'color': ColorRadioSelect(attrs={'class': 'color-radio'})
        }

    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request

    def clean_name(self):
        """项目校验"""
        name = self.cleaned_data.get("name")
        # 1. 当前用户是否已经创建过
        exists = Project.objects.filter(name=name, creator=self.request.tracer.user).exists()
        if exists:
            raise ValidationError("您已创建过该项目！")
        # 2. 额度是否还够
        count = Project.objects.filter(creator=self.request.tracer.user).count()
        if count >= self.request.tracer.price_policy.project_num:
            raise ValidationError("用户额度不足！")

        return name