from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.utils import timezone

from accounts.models import Chat, Company


# Create your views here.

@login_required(redirect_field_name=None)
def group_chat(request):
    # if request.method == 'POST':
    # company = Company.objects.get(comp_name=request.user.extendedusers.comp_name)
    # print(company)
    # return render(request, 'group_chat.html')
    return render(request, 'group_chat.html')


@login_required(redirect_field_name=None)
def private_chat(request):
    company = Company.objects.filter(comp_name=request.user.extendedusers.comp_name)
    print(company.values())
    return render(request, 'private_chat.html')


@login_required(redirect_field_name=None)
def get_messages_company(request, comp_name):
    messages = Chat.objects.filter(comp_obj__comp_name=comp_name).order_by('date')
    # print(messages)
    # return HttpResponse('Message sent successfully')
    return JsonResponse({"messages": list(messages.values())})


@login_required(redirect_field_name=None)
def send(request):
    company = Company.objects.get(comp_name=request.user.extendedusers.comp_name, emp_position='Owner')
    # company = Company.objects.get(comp_name=request.user.extendedusers.comp_name).firs
    # print('sent:', company.values())
    # fetch data from input fields
    message = request.POST['message']
    print('message:', message)
    F_usr = request.user.id
    F_usr_name = request.user.username
    print('f_usr:', F_usr)
    # create chat object,save it.
    new_message = Chat.objects.create(comp=True, comp_obj_id=company.id, date=timezone.now(), F_usr=F_usr,
                                      F_usr_name=F_usr_name, data=message)
    print(new_message)
    new_message.save()
    return HttpResponse('Message sent successfully')


def data_fetching(request):
    return render(request, 'data_fetching.html')
