from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager,AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self,first_name,last_name,username,email,phone_number=None,password=None):
        if not email:
            raise ValueError('User must have an email address')
        if not username:
            raise ValueError('User must have username')
        user=self.model(
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number
        )
        user.set_password(password)
        user.save(using=self._db)

        return user
    
    def create_superuser(self,first_name,last_name,username,email,password=None):
        user=self.create_user(
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name,
            password = password
        )
          
        user.is_superuser=True
        user.is_staff=True
        user.is_active=True
        user.is_admin=True
        user.save(using=self._db)

        return user
    

class User(AbstractBaseUser):
    RESTURANT=1
    CUSTOMER=2
    ROLE_CHOICE=(
        (RESTURANT,'Resturent'),
        (CUSTOMER,'Customer')
    )

    first_name=models.CharField(max_length=50)
    last_name=models.CharField(max_length=50)
    username=models.CharField(max_length=50)
    email=models.EmailField(max_length=100,unique=True)
    phone_number=models.CharField(max_length=12,blank=True,null=True)
    role=models.PositiveSmallIntegerField(choices=ROLE_CHOICE,blank=True,null=True)
    date_joined=models.DateTimeField(auto_now_add=True)
    last_login=models.DateTimeField(auto_now=True)
    is_admin=models.BooleanField(default=False)
    is_active=models.BooleanField(default=False)
    is_staff=models.BooleanField(default=False)
    is_superuser=models.BooleanField(default=False)

    USERNAME_FIELD='email'

    REQUIRED_FIELDS=['username', 'first_name', 'last_name']

    objects=UserManager()
    def __str__(self):
        return self.email
    def has_perm(self,perm,obj=None):
        return self.is_admin
    def has_module_perms(self,app_label):
        return True




class UserProfile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,blank=True,null=True)
    profile_picture=models.ImageField(upload_to='user/profile_picture',blank=True,null=True)
    cover_photo=models.ImageField(upload_to='user/cover_photo',blank=True,null=True)
    adress_line_1=models.CharField(max_length=100,blank=True,null=True)
    adress_line_2=models.CharField(max_length=100,blank=True,null=True)
    country=models.CharField(max_length=100,blank=True,null=True)
    state=models.CharField(max_length=100,blank=True,null=True)
    city=models.CharField(max_length=100,blank=True,null=True)
    pin_code=models.CharField(max_length=100,blank=True,null=True)
    lattiutde=models.CharField(max_length=100,blank=True,null=True)
    longtitude=models.CharField(max_length=100,blank=True,null=True)
    created_at=models.DateTimeField(auto_now_add=True)
    modifed_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username