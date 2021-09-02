from django.contrib.auth.models import User
from django.test import TestCase
from Product.models import Categories, Book
from User.models import UserBase


class TestCategoriesModel(TestCase):

    def setUp(self):
        Categories.objects.create(title='novel', slug='novel')

    def test_category_model_title(self):
        novel = Categories.objects.get(title="novel")
        self.assertEqual(novel.title(), 'novel')


class TestBookModel(TestCase):
    def setUp(self):
        Categories(title='novel', )
        UserBase.objects.create(user_name='ashti')
        Book.objects.create(title='django beginners', in_stock=True, is_active=True, inventory=10,
                            slug='django-beginners', price='20.00', image='django')

    def test_products_model_entry(self):
        book1 = Book.objects.get(title="'django beginners'")
        self.assertEqual(book1.title(), 'django beginners')

