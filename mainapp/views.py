from django.http import JsonResponse
from django.shortcuts import render

from .forms import RegisterModelForm, SendMsgForm, LoginSmsForm


# Create your views here.
def send_massage(request):
    send_msg_form = SendMsgForm(request, data=request.GET)
    if send_msg_form.is_valid():
        return JsonResponse({'status': True})

    return JsonResponse({'status': False, 'error': send_msg_form.errors})


def register(request):
    if request.method == 'GET':
        register_form = RegisterModelForm()
        context = {'register_form': register_form}
        return render(request, 'mainapp/register.html', context)
    elif request.method == 'POST':
        register_form = RegisterModelForm(request.POST)
        if register_form.is_valid():
            # 密码存储为密文
            register_form.save()
            return JsonResponse({'status': True, 'data': '/login/'})

        return JsonResponse({'status': False, 'error': register_form.errors})

    return JsonResponse({})


def login_sms(request):
    login_sms_form = LoginSmsForm()
    context = {'login_sms_form': login_sms_form}
    return render(request, "mainapp/login_sms.html", context)