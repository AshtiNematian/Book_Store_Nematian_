from django.shortcuts import get_object_or_404, render
from .models import Categories, Book


def categories(request):
    return {
        'categories': Categories.objects.all()
    }


def product_all(request):
    books = Book.products.all()
    return render(request, 'home.html', {'books': books})


def category_list(request, category_slug=None):
    category = get_object_or_404(Categories, slug=category_slug)
    products = Book.objects.filter(categories=category)
    return render(request, 'category.html', {'category': category, 'products': products})


def product_detail(request, slug):
    product = get_object_or_404(Book, slug=slug, in_stock=True)
    return render(request, 'single.html', {'product': product})


def search(request):
    q = request.GET['q']
    data = Book.objects.filter(title__icontains=q).order_by('-id')
    return render(request, 'search.html', {'data': data})
