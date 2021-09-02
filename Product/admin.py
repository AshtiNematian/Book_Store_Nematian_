from django.contrib import admin
from Product.models import Categories, Book, Author

@admin.register(Categories)
class CtegoriesAdmin(admin.ModelAdmin):
    list_display = ("title",)
    search_fields = ['title']
    ordering = ('id',)


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("title",'author','is_active','in_stock','inventory','price','dis')
    search_fields = ['title']
    ordering = ('id',)
    list_filter = ['is_active']
    empty_value_display = '-empty-'


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ['name']
    ordering = ('id',)