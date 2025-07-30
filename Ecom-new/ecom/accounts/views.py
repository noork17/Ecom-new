import uuid

from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from base.emails import account_activation_email
from .models import Profile
# Create your views here.
def index(request):
    if request.method == 'POST':
        username = request.POST.get('username');
        password = request.POST.get('password');
        user = User.objects.filter(username=username)
        if not user.exists():
            messages.warning(request, 'Account Not Found')
            return HttpResponseRedirect(request.path_info)
        user=User.objects.get(username=username)
        if not user.profile.is_email_verified:
            messages.warning(request, 'Email Not Verified')
            return HttpResponseRedirect(request.path_info)
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, 'Login Successful')
            return redirect("home")
        messages.warning(request, 'Invalid Credentials')
        return HttpResponseRedirect(request.path_info)
    return render(request, 'login.html')

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username');
        first_name = request.POST.get('first_name');
        last_name = request.POST.get('last_name');
        email = request.POST.get('email');
        password = request.POST.get('password');
        user = User.objects.filter(username=username);
        if  user.exists():
            messages.warning(request, 'Account Already Exists')
            return HttpResponseRedirect(request.path_info)
        user_obj= User.objects.create(username=username, email=email, first_name=first_name, last_name=last_name)
        user_obj.set_password(password)
        user_obj.save()

        profile = Profile.objects.create(
            user=user_obj
        )
        profile.email_token = str(uuid.uuid4())
        profile.save()

        account_activation_email(email,profile.email_token)
        messages.success(request, 'Account Created')
        return HttpResponseRedirect(request.path_info)


    return render(request, 'registation.html')
def password_reset(request):
    pass
def activation_email(request,email_token):
    try:
        #email_token=request.GET.get('token')
        user=Profile.objects.get(email_token=email_token)
        user.is_email_verified = True
        user.save()
        messages.success(request, 'Email Verified')
        return redirect('login')
    except Exception as e:
        return HttpResponse("invalid email token")
def home(request):
    return render(request, 'home.html')
def logout_user(request):
    logout_user(request)
    messages.success(request, 'You have been logged out')
    return redirect('home')

