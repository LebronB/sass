from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from mainapp.forms.project import ProjectModelForm
from mainapp.models import Project, ProjectUser


def project_list(request):
    if request.method == "GET":
        """查看项目列表：包括我创建的，我参与的，星标的"""
        project_dict = {"star": [], "my": [], "join": []}
        my_project = Project.objects.filter(creator=request.tracer.user)
        for row in my_project:
            if row.star:
                project_dict["star"].append({"value": row, "type": "my"})
            else:
                project_dict["my"].append(row)

        join_project = ProjectUser.objects.filter(user=request.tracer.user)
        for item in join_project:
            if item.star:
                project_dict["star"].append({"value": item.project, "type": "join"})
            else:
                project_dict["join"].append(item.project)

        form = ProjectModelForm(request)
        context = {'form': form, 'project_dict': project_dict}
        return render(request, 'mainapp/project_list.html', context)
    form = ProjectModelForm(request, data=request.POST)
    if form.is_valid():
        form.instance.creator = request.tracer.user
        form.save()
        return JsonResponse({'status': True})
    return JsonResponse({'status': False, 'error': form.errors})


def project_star(request, project_type, project_id):
    """星标项目"""
    if project_type == 'my':
        # 防止其他用户修改别人的项目，必须是当前用户才能更改
        Project.objects.filter(id=project_id, creator=request.tracer.user).update(star=True)
        return redirect('mainapp:project_list')

    if project_type == 'join':
        ProjectUser.objects.filter(project_id=project_id, user=request.tracer.user).update(star=True)
        return redirect('mainapp:project_star')

    return HttpResponse("错误请求")


def project_unstar(request, project_type, project_id):
    """取消星标"""
    if project_type == 'my':
        # 防止其他用户修改别人的项目，必须是当前用户才能更改
        Project.objects.filter(id=project_id, creator=request.tracer.user).update(star=False)
        return redirect('mainapp:project_list')

    if project_type == 'join':
        ProjectUser.objects.filter(project_id=project_id, user=request.tracer.user).update(star=False)
        return redirect('mainapp:project_star')

    return HttpResponse("错误请求")