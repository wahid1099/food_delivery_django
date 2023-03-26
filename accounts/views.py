from django.shortcuts import render,redirect
from django.contrib import messages
# Create your views here.
from .forms import  UserForm
from .models import User
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
            messages.success(request,'Your account has been created successfully...')
            return redirect('home')
        else:
            messages.error(request,'Invalid data input')
    else:
        form=UserForm()
    context={
        'form': form,
    }
    return render(request, 'accounts/registration.html',context)

    
