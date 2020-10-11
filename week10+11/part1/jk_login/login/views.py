from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from .form import LoginForm
from django.contrib.auth import authenticate, login

def index(request):
    return HttpResponse("Hello Django!")

def login(request):
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            # 读取表单的返回值
            cd = login_form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user:
                # 登陆用户
                welcome(request)
                return HttpResponse(f'登录成功{user}')
            else:
                return HttpResponse(f'登录失败{user}, {cd}')
    # GET
    if request.method == "GET":
        login_form = LoginForm()
        return render(request, 'form2.html', {'form': login_form})
        # return render(request, 'form1.html')

def welcome(request):
    return render(request, 'form1.html', locals())
