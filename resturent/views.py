from django.shortcuts import render

# Create your views here.

def registerResturent(request):
    return render(request, 'RegisterResturent/ResturentRegistration.html')

def register_selectpackage(request):
    return render(request,'RegisterResturent/register-select-package.html')

def register_paymentinfo(request):
        return render(request,'RegisterResturent/register-payment-info.html')

def register_activation(request):
        return render(request,'RegisterResturent/register-activation.html')


  
