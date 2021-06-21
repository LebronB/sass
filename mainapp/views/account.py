from io import BytesIO

from django.db.models import Q
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect

from utils.verification.verification import check_code
from mainapp.forms.account import RegisterModelForm, SendMsgForm, LoginSmsForm, LoginForm
from mainapp.models import UserInfo, Transaction, PricePolicy
import uuid
import datetime

# Create your views here.


def home(request):
    return render(request, 'mainapp/index.html', )


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
            instance = register_form.save()

            # 创建交易记录
            policy_object = PricePolicy.objects.filter(category=1, title="个人免费版").first()
            Transaction.objects.create(
                status=2,
                order=str(uuid.uuid4()),
                user=instance,
                price_policy=policy_object,
                count=0,
                price=0,
                start_datetime=datetime.datetime.now()
            )

            return JsonResponse({'status': True, 'data': '/login/'})

        return JsonResponse({'status': False, 'error': register_form.errors})

    return JsonResponse({})


def login_sms(request):
    """短信登录"""
    if request.method == 'GET':
        login_sms_form = LoginSmsForm()
        context = {'login_sms_form': login_sms_form}
        return render(request, "mainapp/login_sms.html", context)
    elif request.method == 'POST':
        login_sms_form = LoginSmsForm(request.POST)
        if login_sms_form.is_valid():
            # 通过手机号直接可以获取到用户对象，而不用再做一次查询
            user_object = login_sms_form.cleaned_data['mobile_phone']

            # 用户名写入session
            request.session['user_id'] = user_object.id
            # 两周后过期
            request.session.set_expiry(60 * 60 * 24 * 14)
            return JsonResponse({'status': True, 'data': '/index/'})
        else:
            return JsonResponse({'status': False, 'error': login_sms_form.errors})


def login(request):
    """用户名或手机登录"""
    if request.method == 'GET':
        login_form = LoginForm(request)
        context = {'login_form': login_form}
        return render(request, "mainapp/login.html", context)
    elif request.method == 'POST':
        login_form = LoginForm(request, data=request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']

            # user_object = UserInfo.objects.filter(username=username, password=password).first()
            user_object = UserInfo.objects.filter(Q(email=username) | Q(mobile_phone=username)).filter(
                password=password).first()

            if user_object:
                # 用户名写入session
                request.session['user_id'] = user_object.id
                # 两周后过期
                request.session.set_expiry(60 * 60 * 24 * 14)

                return redirect('mainapp:index')
            login_form.add_error('username', '用户名或密码错误')

        context = {'login_form': login_form}
        return render(request, "mainapp/login.html", context)


def image_code(request):
    """生成图片验证码"""
    image_object, code = check_code()
    # 写入内存
    stream = BytesIO()
    image_object.save(stream, 'png')
    # 写入session
    request.session['image_code'] = code
    # 图片验证码60s失效
    request.session.set_expiry(60)

    return HttpResponse(stream.getvalue())


def logout(request):
    request.session.flush()
    return redirect("mainapp:index")