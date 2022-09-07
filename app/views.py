from django.http.request import host_validation_re
from django.shortcuts import render,redirect
from .models import chat,group
import json
from .Form import account_creation_form,login_form,password_form
from .Form import user_change_form,feedbackform
import http.client
import socket
from django.contrib import auth
from django.http import HttpResponseRedirect,HttpResponse
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail, BadHeaderError
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.conf import settings

def main(request):
    return render(request,'main.html')
    
def home(request):
    return render(request,'home.html')

def index(request,group_name):
    print(request.user)
    print(group_name)
    chat_list = []
    grp = group.objects.filter(name=group_name).first()
    print("group name received from input",grp)
    if grp:
        print("in if block ")
        chat_list=chat.objects.filter(group=grp)
        print("okay show chat list",chat_list)
    else:
        print("in else block ")
        group.objects.create(name=group_name)
    strr = str(request.user)
    userk = bytes(strr, 'utf-8')
    print(type(userk))
    userkk = userk.decode(encoding = "utf-8")
    print(type(userkk))
    return render(request,'index.html',{'chatmsg':chat_list,'group':group_name,'userr':userkk})

def dindex(request,group_name):
    print(request.user)
    print(group_name)
    chat_list = []
    grp = group.objects.filter(name=group_name).first()
    print("group name received from input",grp)
    if grp:
        print("in if block ")
        chat_list=chat.objects.filter(group=grp)
        print("okay show chat list",chat_list)
    else:
        print("in else block ")
        group.objects.create(name=group_name)
    strr = str(request.user)
    userk = bytes(strr, 'utf-8')
    print(type(userk))
    userkk = userk.decode(encoding = "utf-8")
    print(type(userkk))
    return render(request,'dindex.html',{'chatmsg':chat_list,'group':group_name,'userr':userkk})

def customroom(request):
    if request.method == "POST":
        grp = request.POST['custom']
        print(grp)
        print(type(grp))
        return HttpResponseRedirect('http://127.0.0.1:8000/home/k/'+grp)

def formin(request):
    return render(request,'formin.html')

def signup(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('account')
    else:
        if request.method=="POST":
            fm = account_creation_form(request.POST)
            if fm.is_valid():
                fm.save()
                return render(request,'account.html')
            else:
                print("problem here")
                data = fm.cleaned_data.get("form_field")
                print(data)
                return render(request,'ok.html',{'fm':fm})
        else:
            fm = account_creation_form()
            return render(request,'signup.html',{'fm':fm})

def login(request):
    if request.method == 'POST':
        user_fm = login_form(data=request.POST)
        if user_fm.is_valid():
            uname = user_fm.cleaned_data['username']
            upass = user_fm.cleaned_data['password']
            user = auth.forms.authenticate(username=uname,password=upass)
            if user is not None:
                auth.login(request,user)
                return HttpResponseRedirect('account')
            else:
                user_fm = login_form()
                return render(request,'ok.html',{'fm':user_fm})
        else:
            user_fm=login_form()
            return render(request,'ok.html',{'fm':user_fm})
    else:
        user_fm = login_form()
        return render(request,'login.html',{'fm':user_fm})

def account(request):
    return HttpResponseRedirect('home')

def account_check(request):
    if request.user.is_authenticated:
        user_acc = user_change_form(instance=request.user)
        return render(request,'account_detail.html',{'data':user_acc})
    else:
        return HttpResponseRedirect('login')

def password(request):
    if request.method == "POST":
        fm=password_form(user=request.user,data=request.POST)
        if fm.is_valid():
            msg = "valid password"
            fm.save()
            return HttpResponseRedirect('login')
        else:
            msg = "not valid password"
            warn = "Enter password combination of letter and number"
            fm = password_form(request.user)
            return render(request,'password.html',{'fm':fm,'msg':msg,'warn':warn})
    else:
        msg = "Enter password combination of letter and number"
        warn = ""
        fm = password_form(request.user)
        return render(request,'password.html',{'fm':fm,'msg':msg,'warn':warn})

def editaccount(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            user = user_change_form(request.POST,instance=request.user)
            if user.is_valid():
                user.save()
                return HttpResponseRedirect('login')
            else:
                user_acc = user_change_form(instance=request.user)
                return render(request,'editprofile.html',{'data':user_acc})
        else:
            user_acc = user_change_form(instance=request.user)
            return render(request,'editprofile.html',{'data':user_acc})
    else:
        return HttpResponseRedirect('login')

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('login')

def password_reset_request(request):
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = User.objects.filter(Q(email=data))
            if associated_users.exists():
                for user in associated_users:
                    subject = "Password Reset Requested"
                    email_template_name = "password_reset_email.txt"
                    c = {
					"email":user.email,
					'domain':'groupchat.ind.in',
					'site_name': 'Website',
					"uid": urlsafe_base64_encode(force_bytes(user.pk)),
					"user": user,
					'token': default_token_generator.make_token(user),
					'protocol': 'http',
					}
                    email = render_to_string(email_template_name, c)
                    vemail="https://groupmasti.herokuapp.com/reset/"+c['uid']+"/"+c['token']
                    print(vemail)
                    try:
                        send_mail(subject, email, 'admin@example.com' , [user.email], fail_silently=False)
                    except BadHeaderError:
                        return HttpResponse('Invalid header found.')
                    return redirect ("/password_reset/done/")
    password_reset_form = PasswordResetForm()
    return render(request=request, template_name="password_reset.html", context={"password_reset_form":password_reset_form})

def privacy(request):
    return render(request,'privacy.html')

def policy(request):
    return render(request,'policy.html')

def support(request):
    return render(request,'support.html')
    
def feedback(request):
    if request.method == "POST":
        fm = feedbackform(request.POST,request.FILES)
        if fm.is_valid():
            x = fm.cleaned_data['Email']
            fm.save()
            return render(request,'thank.html')
        else:
            fm=feedbackform()
            return render(request,'feedback.html',{'fm':fm})
    else:
        fm=feedbackform()
        return render(request,'feedback.html',{'fm':fm})

def report(request):
    reportperson = request.user
    return render(request,'chat.html',{'report':reportperson})