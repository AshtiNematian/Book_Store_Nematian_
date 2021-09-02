import datetime

from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import redirect, render, get_object_or_404
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.views.generic import ListView, CreateView, DetailView

from Orders.views import user_orders
from Product.models import Book, Categories
from .forms import RegistrationForm, UserEditForm, UserAddressForm, AddCategoriesForm, AddBookForm
from .models import UserBase, Address
from User.tokens import account_activation_token
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse, reverse_lazy


# Customer_views
@login_required
def dashboard(request):
    user = request.user
    orders = user_orders(request)
    if user.is_superuser:
        return render(request,
                      'index.html',
                      {'section': 'profile'})

    if user.is_staff:
        return render(request,
                      'staff.html',
                      {'section': 'profile'})

    return render(request,
                  'dashboard.html',
                  {'section': 'profile', 'orders': orders})


@login_required
def edit_details(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        if user_form.is_valid():
            user_form.save()
    else:
        user_form = UserEditForm(instance=request.user)

    return render(request,
                  'edit_details.html', {'user_form': user_form})


@login_required
def delete_user(request):
    user = UserBase.objects.get(user_name=request.user)
    user.is_active = False
    user.save()
    logout(request)
    return redirect('account:delete_confirmation')


def account_register(request):
    if request.user.is_authenticated:
        return redirect('account:dashboard')

    if request.method == 'POST':
        registerForm = RegistrationForm(request.POST)
        if registerForm.is_valid():
            user = registerForm.save(commit=False)
            user.email = registerForm.cleaned_data['email']
            user.set_password(registerForm.cleaned_data['password'])
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            subject = 'Activate your Account'
            message = render_to_string('account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject=subject, message=message)
            return HttpResponse('registered succesfully and activation sent')
    else:
        registerForm = RegistrationForm()
    return render(request, 'register.html', {'form': registerForm})


def account_activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = UserBase.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, user.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('account:dashboard')
    else:
        return render(request, 'activation_invalid.html')


@login_required
def view_address(request):
    addresses = Address.objects.filter(customer=request.user)
    return render(request, "addresses.html", {"addresses": addresses})


@login_required
def add_address(request):
    if request.method == "POST":
        address_form = UserAddressForm(data=request.POST)
        if address_form.is_valid():
            address_form = address_form.save(commit=False)
            address_form.customer = request.user
            address_form.save()
            return HttpResponseRedirect(reverse("account:addresses"))
    else:
        address_form = UserAddressForm()
    return render(request, "edit_addresses.html", {"form": address_form})


@login_required
def edit_address(request, id):
    if request.method == "POST":
        address = Address.objects.get(pk=id, customer=request.user)
        address_form = UserAddressForm(instance=address, data=request.POST)
        if address_form.is_valid():
            address_form.save()
            return HttpResponseRedirect(reverse("account:addresses"))
    else:
        address = Address.objects.get(pk=id, customer=request.user)
        address_form = UserAddressForm(instance=address)
    return render(request, "edit_addresses.html", {"form": address_form})


@login_required
def delete_address(request, id):
    address = Address.objects.filter(pk=id, customer=request.user).delete()
    return redirect("account:addresses")


@login_required
def set_default(request, id):
    Address.objects.filter(customer=request.user, default=True).update(default=False)
    Address.objects.filter(pk=id, customer=request.user).update(default=True)
    return redirect("account:addresses")


# Admin_views

def staff(request):
    workers = UserBase.objects.filter(is_staff=True)
    context = {
        'staffs': workers,
    }
    return render(request, 'staff_list.html', context)


def category_create(request):
    form = AddCategoriesForm()
    if request.method == 'POST':
        data = request.POST
        category = Categories.objects.create(title=data['title'], slug=data['slug'])
        category.save()
    category = Categories.objects.all()
    context = {'category': category, 'form': form}
    return render(request, 'category_new.html', context)


class BookCreateView(CreateView):
    model = Book
    template_name = 'book_new.html'
    form_class = AddBookForm
    success_url = reverse_lazy('account:book_new')

    def get_object(self):
        return Book.objects.get(pk=self.request)


class CategoryListView(ListView):
    model = Categories
    template_name = 'admin_cat.html'
    context_object_name = "categories"

    def get_queryset(self):
        queryset = {'category_list': Categories.objects.all()}
        return queryset


def product_detail(request, slug):
    user = UserBase.objects.all()
    product = get_object_or_404(Book, slug=slug, in_stock=True)
    return render(request, 'single.html', {'product': product, 'user': user})


def active_user(request):
    daily_users = UserBase.objects.filter(date_joined__day=datetime.today().day).count()
    return render(request, 'index.html', {'user': daily_users})


def user(request):
    time = datetime.date.today()
    new_order = UserBase.objects.filter(created=time, paid=True)
    return render(request, 'index.html', {'order': new_order})
