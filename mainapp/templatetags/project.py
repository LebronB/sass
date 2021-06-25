from django.template import Library
from django.urls import reverse

from mainapp.models import Project, ProjectUser
register = Library()


@register.inclusion_tag('inclusion/all_project_list.html')
def all_project_list(request):
    """
    获取我创建的项目
    获取我参与的项目
    :return:
    """
    # 我创建的
    my_project_list = Project.objects.filter(creator=request.tracer.user)
    # 我参与的
    join_project_list = ProjectUser.objects.filter(user=request.tracer.user)

    return {'my': my_project_list, 'join': join_project_list, 'request': request}


@register.inclusion_tag('inclusion/manage_menu_list.html')
def manage_menu_list(request):
    data_list = [
        {'title': '概览', 'url': reverse('mainapp:dashboard', kwargs={'project_id': request.tracer.project.id})},
        {'title': '文件', 'url': reverse('mainapp:files', kwargs={'project_id': request.tracer.project.id})},
        {'title': 'wiki', 'url': reverse('mainapp:wiki', kwargs={'project_id': request.tracer.project.id})},
        {'title': '统计', 'url': reverse('mainapp:statistics', kwargs={'project_id': request.tracer.project.id})},
        {'title': '问题', 'url': reverse('mainapp:issues', kwargs={'project_id': request.tracer.project.id})},
        {'title': '配置', 'url': reverse('mainapp:settings', kwargs={'project_id': request.tracer.project.id})},
    ]

    for item in data_list:
        if request.path_info.startswith(item['url']):
            item['class'] = 'active'

    return {'data_list': data_list}
