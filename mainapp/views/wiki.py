from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt


from mainapp.forms.wiki import WikiModelForm
from mainapp.models import Wiki
from utils.encrypt import uid
from utils.tencent.cos import upload_files


def wiki(request, project_id):
    """首页"""
    wiki_id = request.GET.get('wiki_id')
    if not wiki_id or not wiki_id.isdecimal():
        return render(request, 'mainapp/wiki.html')

    wiki_obj = Wiki.objects.filter(project_id=project_id, id=wiki_id).first()
    context = {'wiki_obj': wiki_obj}
    return render(request, 'mainapp/wiki.html', context)


def wiki_add(request, project_id):
    if request.method == 'GET':
        form = WikiModelForm(request)
        context = {'form': form}
        return render(request, 'mainapp/wiki_form.html', context)
    form = WikiModelForm(request, data=request.POST)
    if form.is_valid():
        if form.instance.parent:
            form.instance.depth = form.instance.parent.depth + 1
        else:
            form.instance.depth = 1

        form.instance.project = request.tracer.project
        form.save()
        url = reverse('mainapp:wiki', kwargs={'project_id': project_id})
        return redirect(url)


def wiki_catalog(request, project_id):
    """wiki目录展示"""
    data = Wiki.objects.filter(project=request.tracer.project).values('id', 'title', 'parent_id').order_by('depth',
                                                                                                           'id')
    return JsonResponse({'status': True, 'data': list(data)})


def wiki_delete(request, project_id, wiki_id):
    """wiki删除"""
    Wiki.objects.filter(project_id=project_id, id=wiki_id).delete()
    return redirect(reverse('mainapp:wiki', kwargs={'project_id': project_id}))


def wiki_edit(request, project_id, wiki_id):
    """wiki编辑"""
    wiki_obj = Wiki.objects.filter(project_id=project_id, id=wiki_id).first()
    if not wiki_obj:
        return redirect(reverse('mainapp:wiki', kwargs={'project_id': project_id}))

    if request.method == 'GET':
        form = WikiModelForm(request, instance=wiki_obj)
        context = {'form': form}
        return render(request, 'mainapp/wiki_form.html', context)
    form = WikiModelForm(request, data=request.POST, instance=wiki_obj)
    if form.is_valid():
        if form.instance.parent:
            form.instance.depth = form.instance.parent.depth + 1
        else:
            form.instance.depth = 1
        form.save()
        url = reverse('mainapp:wiki', kwargs={'project_id': project_id})
        pre_url = ("{0}?wiki_id={1}".format(url, wiki_id))
        return redirect(pre_url)
    else:
        return render(request, 'mainapp/wiki_form.html', {'form': form})


@csrf_exempt
def wiki_upload(request, project_id):
    """上传本地图片"""
    result = {
        'success': 0,
        'massage': None,
        'url': None
    }

    image = request.FILES.get('editormd-image-file')
    if not image:
        # 没有上传文件，处理上传失败的情况
        result['massage'] = "文件不存在"
        return JsonResponse(result)

    ext = image.name.rsplit('.')[-1]
    key = "{}.{}".format(uid(request.tracer.user.mobile_phone), ext)

    image_url = upload_files(request.tracer.project.bucket,
                             request.tracer.project.region,
                             image,
                             key
                             )

    result['success'] = 1
    result['url'] = image_url

    return JsonResponse(result)
