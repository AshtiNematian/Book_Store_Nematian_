from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.urls import reverse


class Categories(models.Model):
    title = models.CharField(max_length=50, null=True, blank=True)
    slug = models.SlugField(unique=True, blank=True, null=True)

    def get_absolute_url(self):
        return reverse('store:category_list', args=[self.slug])

    def __str__(self):
        return self.title


class Author(models.Model):
    name = models.CharField(max_length=50, null=True, blank=True)
    slug = models.SlugField(unique=True, blank=True, null=True)

    def __str__(self):
        return self.name


class ProductManager(models.Manager):
    def get_queryset(self):
        return super(ProductManager, self).get_queryset().filter(is_active=True)


class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.DO_NOTHING,
                               related_name='book_author', blank=True, null=True)
    price = models.DecimalField(max_digits=7, decimal_places=3)
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    description = models.TextField(max_length=300, blank=True)
    in_stock = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    categories = models.ManyToManyField(Categories, related_name='category')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    slug = models.SlugField(unique=True, blank=True)
    dis = models.DecimalField(max_digits=7, decimal_places=3, null=True, blank=True)
    discount_percent = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)], null=True,
                                           blank=True)
    inventory = models.IntegerField(default=0)
    objects = models.Manager()
    products = ProductManager()

    def get_image(self):
        if self.image:
            return 'http://127.0.0.1:8000' + self.image.url
        return ''

    def disc(self):
        self.price - self.dis

    class Meta:
        ordering = ('-created',)

    def get_absolute_url(self):
        return reverse('store:product_detail', args=[self.slug])

    def __str__(self):
        return self.title

    def price_after_dis(self):
        dis = self.dis
        if dis is None:
            dis = 0
        return self.price - dis

    def percent_discount(self):
        discount = self.discount_percent
        if discount is None:
            discount = 0
        return self.price - self.price * discount / 100

    def remove_items_from_inventory(self, count=1, save=True):
        self.inventory -= count
        if save == True:
            self.save()
        return self.inventory
