from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, AbstractUser, PermissionsMixin

# Create your models here.
## Creater Manager---------------------------------------------------------------
class CustomUserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, mobile, address,  password=None, **extra_fields):
        """
        Creates and saves a User with the given email, first_name, last_name, mobile, address and password.
        """
        if not email:
            raise ValueError("Users must have an email address")
        if not password:
            raise ValueError("Password is Requared")
        
        email = email.lower()
        first_name = first_name.title()
        last_name = last_name.title()

        user = self.model(
            email=self.normalize_email(email),
            first_name = first_name,
            last_name = last_name, 
            mobile = mobile,
            address = address,
            **extra_fields
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, mobile, address,  password=None, **extra_fields):
        """
        Creates and saves a superuser with the given email, first_name, last_name and password.
        """
        user = self.create_user(
            email = email,
            first_name = first_name,
            last_name = last_name,
            password = password,
            mobile = mobile,
            address = address,
            **extra_fields
        )
        user.is_admin = True
        user.is_active = True
        user.save(using=self._db)
        return user
    

    
## Create A custom User Model---------------------------------------------------------
class User(AbstractBaseUser, PermissionsMixin):
    ## AbstructBaseUser has provite some default field ( password, last_login, is_active )
    email = models.EmailField(
        verbose_name="email address",
        max_length=255,
        unique=True,
    )

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    mobile = models.CharField(max_length=50, null=True, blank=True)
    address = models.TextField(max_length=200, null=True, blank=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    is_customer = models.BooleanField(default=False)
    is_seller = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"  ## এটি Django user name হিসেবে set হবে
    REQUIRED_FIELDS = ["first_name","last_name", "mobile", "address"]

    def __str__(self):
        return self.email
    
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    def get_short_name(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        # return True      ## Default
        return self.is_admin

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        # return True      ## Default
        return self.is_admin

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'




# +++++++++++++++++++++++++++++++   Others Model   ++++++++++++++++++++++++++++++++


class UserOTP(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    time_st = models.DateTimeField(auto_now = True)
    otp = models.SmallIntegerField()



class Customer(models.Model):
    gen=(
        ('Male' , 'Male'),
        ('Femal' , 'Femal'),
        ('Other' , 'Other'),
    )
    user = models.OneToOneField("Accounts.User", on_delete=models.CASCADE)
    profile_pictur = models.ImageField(null=True, blank=True)
    cover_pictur = models.ImageField(null=True, blank=True)
    death_of_birth = models.CharField(max_length=50, null=True, blank=True)
    gender = models.CharField(max_length=20, choices=gen)

    def __str__(self):
        return self.user.email



class Seller(models.Model):
    user = models.OneToOneField("Accounts.User", on_delete=models.CASCADE)
    shope_name = models.CharField(max_length=100)
    Trade_license = models.ImageField()
    Owner_NID = models.ImageField()

    def __str__(self):
        return self.user.email