from django.urls import path
from . import views

urlpatterns =[
     path('registerresutrent/',views.registerResturent,name="registerresutrent"),
     path('selectpackage/',views.register_selectpackage,name="selectpackage"),
     path('payment_register/',views.register_paymentinfo,name="payment_register"),
     path('register_activation/',views.register_activation,name="register_activation"),

     
]