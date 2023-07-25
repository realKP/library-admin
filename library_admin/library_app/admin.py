from django.contrib import admin

# Register your models here.
from .models import Member, Library, Book, Author, Resource, Rental, RentalItem, BookAuthor

admin.site.register(Member)
admin.site.register(Library)
admin.site.register(Book)
admin.site.register(Author)
admin.site.register(Resource)
admin.site.register(Rental)
admin.site.register(RentalItem)
admin.site.register(BookAuthor)
