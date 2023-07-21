from django.contrib import admin

# Register your models here.
from .models import Member, Library, Book

admin.site.register(Member)
admin.site.register(Library)
admin.site.register(Book)