import uuid

from django.shortcuts import render
from django.utils import timezone
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager, PermissionsMixin)
from django.core.mail import send_mail
from django.db import models
from django.utils.translation import gettext_lazy as _

ADDRESS_CHOICES = (
    ('B', 'Billing'),
    ('S', 'Shipping'),
)


class CustomAccountManager(BaseUserManager):

    def create_superuser(self, email, user_name, password, **other_fields):

        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError(
                'Superuser must be assigned to is_staff=True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must be assigned to is_superuser=True.')

        return self.create_user(email, user_name, password, **other_fields)

    def create_user(self, email, user_name, password, **other_fields):

        if not email:
            raise ValueError(_('You must provide an email address'))

        email = self.normalize_email(email)
        user = self.model(email=email, user_name=user_name,
                          **other_fields)
        user.set_password(password)
        user.save()
        return user


'''

Its for creating users if is_staff=True user be staff otherwise is customer

'''


class UserBase(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    user_name = models.CharField(max_length=150)
    mobile = models.CharField(max_length=150, blank=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = CustomAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['user_name']

    class Meta:
        verbose_name = "کاربر"
        verbose_name_plural = "کاربران"

    def email_user(self, subject, message):
        send_mail(
            subject,
            message,
            'l@1.com',
            [self.email],
            fail_silently=False,
        )

    def admin(self):
        admn = UserBase.objects.filter(is_staff=True, is_superuser=True)
        return admn

    def staffs(self):
        return self.is_staff

    def customers(self):
        customer = UserBase.objects.filter(is_superuser=False, is_staff=False)
        return not self.is_staff and not self.is_superuser

    def __str__(self):
        return self.user_name


class Address(models.Model):
    """
    Address of customers
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer = models.ForeignKey(UserBase, verbose_name=_("Customer"), on_delete=models.CASCADE)
    full_name = models.CharField(_("Full Name"), max_length=150)
    phone = models.CharField(_("Phone Number"), max_length=50)
    postcode = models.CharField(_("Postcode"), max_length=50)
    address_line = models.CharField(_("Address Line 1"), max_length=255)
    address_line2 = models.CharField(_("Address Line 2"), max_length=255)
    town_city = models.CharField(_("Town/City/State"), max_length=150)
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated at"), auto_now=True)
    default = models.BooleanField(_("Default"), default=False)

    class Meta:
        verbose_name = "آدرس "
        verbose_name_plural = "آدرس ها"

    def __str__(self):
        return f'{self.address_line}-{self.postcode}-{self.town_city}'
