from mainapp.models import Wiki
from .account import BootStrapForm
from django import forms


class WikiModelForm(BootStrapForm, forms.ModelForm):

    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)

        total_data_list = [('', '请选择')]
        wiki_objs = Wiki.objects.filter(project=request.tracer.project)
        # 编辑时去除父目录中自己的选项
        if self.instance.id:
            wiki_objs = wiki_objs.exclude(id__in=[self.instance.id, ])
        data_list = wiki_objs.values_list('id', 'title')
        total_data_list.extend(data_list)
        self.fields['parent'].choices = total_data_list

    class Meta:
        model = Wiki
        exclude = ['project', 'depth',]