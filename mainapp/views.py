import random

from django.conf import settings
from django.shortcuts import HttpResponse, render

from utils.tencent.sms import send_sms_single
from .forms import RegisterModelForm


# Create your views here.
def send_massage(request):
    tpl = request.GET.get('tpl')
    template_id = settings.TENCENT_SMS_TEMPLATE.get(tpl)
    if not template_id:
        return HttpResponse("发送失败，模板不存在")

    code = random.randrange(1000, 9999)
    res = send_sms_single('13540166346', template_id, [code, ])
    if res['result'] == 0:
        return HttpResponse('成功')
    else:
        return HttpResponse(res['errmsg'])


def register(request):
    register_form = RegisterModelForm()
    context = {'register_form': register_form}
    return render(request, 'mainapp/register.html', context)

