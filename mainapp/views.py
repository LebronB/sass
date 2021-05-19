from django.shortcuts import HttpResponse, render
from django.http import JsonResponse
from .forms import RegisterModelForm, SendMsgForm


# Create your views here.
def send_massage(request):
    send_msg_form = SendMsgForm(request, data=request.GET)
    if send_msg_form.is_valid():
        return JsonResponse({'status': True})

    return JsonResponse({'status': False, 'error': send_msg_form.errors})


def register(request):
    register_form = RegisterModelForm()
    context = {'register_form': register_form}
    return render(request, 'mainapp/register.html', context)

