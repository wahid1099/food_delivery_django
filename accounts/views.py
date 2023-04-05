from django.shortcuts import render,redirect
from django.contrib import messages,auth
# Create your views here.
from .forms import  UserForm
from .models import User,UserProfile
from resturent.forms import RestaurantForm
from django.contrib.auth.decorators import login_required
from  .utils import detectUser, send_email
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator

def registerUser(request):
    if request.user.is_authenticated:
        messages.warning(request,'You are already logged in..')
        return redirect('home')
    elif request.method=="POST":
        form=UserForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email=form.cleaned_data['email']
            password = form.cleaned_data['password']
            user=User.objects.create_user(first_name=first_name,last_name=last_name,username=username,email=email,password=password)
            user.role=User.CUSTOMER
            user.save()
            email_subject = "Please active your account"
            email_template ="accounts/emails/account_varification.html"
            send_email(request,user,email_subject,email_template)
            messages.success(request,'Your account has been registered successfully...')
            return redirect('home')
        else:
            messages.error(request,'Invalid data input')
    else:
        form=UserForm()
    context={
        'form': form,
    }
    return render(request, 'accounts/registration.html',context)

def registerRestaurant(request):
    if request.user.is_authenticated:
        messages.waring(request,'You are already logged in')
        return redirect('home')
    elif request.method == 'POST':
        form=UserForm(request.POST)
        restaurant_form=RestaurantForm(request.POST,request.FILES)
        if form.is_valid() and restaurant_form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username=form.cleaned_data['username']
            email=form.cleaned_data['email']
            password=form.cleaned_data['password']
            phone_number=form.cleaned_data['phone_number']
            user=User.objects.create_user(first_name=first_name,last_name=last_name,username=username,email=email,password=password,phone_number=phone_number)
            user.role=User.RESTURANT
            user.save()
            restaurant=restaurant_form.save(commit=False)
            restaurant.user=user
            
            user_profile=UserProfile.objects.get(user=user)
            print(user_profile)
            restaurant.user_profile=user_profile
            restaurant.save()
            email_subject = "Please active your account"
            email_template ="accounts/emails/account_varification.html"
            send_email(request,user,email_subject,email_template)
            messages.success(request,'Your account has been registered successfully')
            return redirect('home')
        else:
            messages.error(request,'Invalid data found')
    else:
        form=UserForm()
        restaurant_form=RestaurantForm()
    context={
            'form':form,
            'restaurant_form':restaurant_form
        }
    return render(request,'accounts/registerRestaurant.html',context)


def activate(request,uidb64,token):
    try:
        uid=urlsafe_base64_decode(uidb64).decode()
        user=User._default_manager.get(pk=uid)
    except (TypeError,ValueError,OverflowError,User.DoesNotExist):
        user=None
    if user is not None and default_token_generator.check_token(user,token):
        user.is_active=True
        user.save()
        return redirect('login')
    else:
        messages.error(request,'Invalid activation Link')
        return redirect('login')
    
def login(request):
    if request.user.is_authenticated:

        messages.warning(request,'You are already logged in')
    elif request.method == 'POST':
        email=request.POST['email']
        password=request.POST['password']
        user=auth.authenticate(email=email,password=password)
        if user is not None:
            auth.login(request,user)
            messages.success(request,'Successfully Logged in!!')
            return redirect('myaccounts')
        else:
            messages.error(request,'Invalid login credentials')
            return redirect('login')
    return render(request, 'accounts/login.html')




    



def logout(request):
    auth.logout(request)
    messages.info(request,'You are logged out')
    return render(request, 'accounts/login.html')

@login_required(login_url=login)
def myaccounts(request):
    user=request.user
    redirectUrl=detectUser(user)
    return redirect(redirectUrl)

@login_required(login_url=login)
def customerDashboard(request):
    return render(request,'accounts/Customer_dashboard.html')



@login_required(login_url=login)
def  restaurantDashboard(request):

    return render(request,'accounts/restaurant_dashboard.html')





    
