
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import BookletForm
from .models import Booklet
from django.contrib.auth import login, authenticate,logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
import os
from django.core.exceptions import SuspiciousOperation
from django.views.decorators.csrf import csrf_exempt
from django.core.validators import validate_email

# Create your views here.
def home(request):
    return render(request, "authentication/index.html")

@csrf_exempt

def signup(request):
    try:
        if request.method == "POST":
            username= request.POST['username']
            fname= request.POST['fname']
            lname= request.POST['lname']
            email= request.POST['email']
            pass1=request.POST['pass1']
            pass2=request.POST['pass2']
            if pass1 != pass2:
                messages.error(request, "Passwords did not match")
                return redirect('signup')
            try:
                validate_email(email)
            except:
                messages.error(request, "Email is invalid")
                return redirect('signup')
            user = User.objects.filter(email=email).exists()
            if user:
                messages.error(request, "Email alredy exists. Try another email adress")
                return redirect('signup')
            
            
            
            myuser=User.objects.create_user(username,email,pass1)
            myuser.first_name= fname
            myuser.last_name= lname
            myuser.save()
            messages.success(request, "your account is created successfully")
            return redirect('signin')
    except:
        messages.error(request, "Enter the credentials freshly")
        return redirect("signup")
    return render(request, "authentication/signup.html")
@csrf_exempt
def signin(request):
    try:
        return render(request, "authentication/signin.html")
    except:
        messages.error(request, "Wrong Credentials")
        return redirect("signin")
@csrf_exempt   
def signined(request):
    try:
        username= request.POST.get("username")
        pass1=request.POST.get("pass1")
        
        user = authenticate(request, username= username, password= pass1)
        if user is not None:
            login(request, user)
            return render(request, "authentication/signined.html")
        else:
            messages.error(request, "Wrong Credentials")
            return redirect("signin")
    except:
        messages.error(request, "Enter the credentials freshly")
        return redirect("signin")

def signout(request):
    logout(request)
    return render(request, 'authentication/index.html')
def list_booklets(request):
    if request.user.is_superuser:
        booklets = Booklet.objects.all()
        return render(request, 'authentication/list_booklets.html', {'booklets': booklets, 'admin': True})
    else:
        booklets = Booklet.objects.all()
        return render(request, 'authentication/list_booklets.html', {'booklets': booklets, 'admin': False})
    #booklets = Booklet.objects.all()
    #return render(request, 'authentication/list_booklets.html', {'booklets': booklets})

@login_required(login_url='/login/')
def delete_booklet(request, booklet_id):
    booklet = Booklet.objects.get(id=booklet_id)
    booklet.delete()
    return redirect('list_booklets')

@login_required(login_url='/login/')
def add_booklet(request):
    if request.method == 'POST':
        form = BookletForm(request.POST, request.FILES)
        if form.is_valid():
            booklet = form.save(commit=False)
            booklet.uploaded_by = request.user
            booklet.save()
            return redirect('list_booklets')
    else:
        form = BookletForm()
    return render(request, 'authentication/add_booklet.html', {'form': form})
'''def download_booklet(request, booklet_id):
    booklet = Booklet.objects.get(id=booklet_id)
    return redirect('list_booklets')
'''