from django import forms
from django.contrib.auth.forms import (AuthenticationForm, PasswordResetForm,
                                       SetPasswordForm)

from Product.models import Book
from .models import UserBase, Address


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control mb-3', 'placeholder': 'نام کاربری', 'id': 'login-username'}))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'رمز ورود',
            'id': 'login-pwd',
        }
    ))


class RegistrationForm(forms.ModelForm):
    user_name = forms.CharField(
        label='حساب کاربری', min_length=4, max_length=50, help_text='اجباری')
    email = forms.EmailField(max_length=100, help_text='Required', error_messages={
        'اجباری': 'لطفا ایمیل خود را وارد کنید'})
    password = forms.CharField(label='رمز عبور', widget=forms.PasswordInput)
    password2 = forms.CharField(
        label='تکرار رمز عبور', widget=forms.PasswordInput)

    class Meta:
        model = UserBase
        fields = ('user_name', 'email',)

    def clean_username(self):
        user_name = self.cleaned_data['user_name'].lower()
        r = UserBase.objects.filter(user_name=user_name)
        if r.count():
            raise forms.ValidationError("این اسم قبلا انتخاب شده")
        return user_name

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('رمز عبور منطبق نیست')
        return cd['password2']

    def clean_email(self):
        email = self.cleaned_data['email']
        if UserBase.objects.filter(email=email).exists():
            raise forms.ValidationError(
                'لطفا ایمیل دیگری وارد کنید این ایمیل تکراریست')
        return email

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user_name'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'نام کاربری'})
        self.fields['email'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'ایمیل', 'name': 'email', 'id': 'id_email'})
        self.fields['password'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'رمز عبور'})
        self.fields['password2'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'تکرار رمز عبور'})


class PwdResetForm(PasswordResetForm):
    email = forms.EmailField(max_length=254, widget=forms.TextInput(
        attrs={'class': 'form-control mb-3', 'placeholder': 'ایمیل', 'id': 'form-email'}))

    def clean_email(self):
        email = self.cleaned_data['email']
        u = UserBase.objects.filter(email=email)
        if not u:
            raise forms.ValidationError(
                'آدرس ایمیل اشتباه است')
        return email


class PwdResetConfirmForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label='New password', widget=forms.PasswordInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'رمز عبور جدید', 'id': 'form-newpass'}))
    new_password2 = forms.CharField(
        label='Repeat password', widget=forms.PasswordInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'رمز عبور حدید', 'id': 'form-new-pass2'}))


class UserEditForm(forms.ModelForm):
    email = forms.EmailField(
        label='Account email (غیر قابل تغییر)', max_length=200, widget=forms.TextInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'ایمیل', 'id': 'form-email', 'readonly': 'readonly'}))

    user_name = forms.CharField(
        label='username', min_length=4, max_length=50, widget=forms.TextInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'نام کاربری', 'id': 'form-username'}))

    password = forms.CharField(
        label='password', min_length=4, max_length=50, widget=forms.TextInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'رمز عبور', 'id': 'form-username'}))

    class Meta:
        model = UserBase
        fields = ('email', 'user_name', 'password')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user_name'].required = True
        self.fields['email'].required = True


class UserAddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ["full_name", "phone", "address_line", "address_line2", "town_city", "postcode"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["full_name"].widget.attrs.update(
            {"class": "form-control mb-2 account-form", "placeholder": "نام و نام خانوادگی"}
        )
        self.fields["phone"].widget.attrs.update(
            {"class": "form-control mb-2 account-form", "placeholder": "شماره تلفن"})
        self.fields["address_line"].widget.attrs.update(
            {"class": "form-control mb-2 account-form", "placeholder": "آدرس"}
        )
        self.fields["address_line2"].widget.attrs.update(
            {"class": "form-control mb-2 account-form", "placeholder": "آدرس"}
        )
        self.fields["town_city"].widget.attrs.update(
            {"class": "form-control mb-2 account-form", "placeholder": "نام شهر"}
        )
        self.fields["postcode"].widget.attrs.update(
            {"class": "form-control mb-2 account-form", "placeholder": "کد پستی"}
        )


class AddCategoriesForm(forms.Form):
    title = forms.CharField(label='title', max_length=20)
    slug = forms.SlugField()


class AddBookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = '__all__'
