# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Member(models.Model):
    member_id = models.AutoField(primary_key=True)
    member_first_name = models.CharField(max_length=255)
    member_last_name = models.CharField(max_length=255)
    member_phone = models.CharField(max_length=10)
    member_email = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'members'

    def __str__(self):
        return (self.member_first_name + ' ' + self.member_last_name)


class Book(models.Model):
    isbn = models.CharField(primary_key=True, max_length=255)
    book_title = models.CharField(unique=True, max_length=255)

    class Meta:
        managed = False
        db_table = 'books'

    def __str__(self):
        return (self.isbn)


class Library(models.Model):
    library_id = models.AutoField(primary_key=True)
    library_name = models.CharField(unique=True, max_length=255)
    library_address = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'libraries'

    def __str__(self):
        return self.library_name


class Resource(models.Model):
    resource_id = models.AutoField(primary_key=True)
    isbn = models.ForeignKey(Book, models.PROTECT, db_column='isbn')
    library = models.ForeignKey(Library, models.PROTECT)
    quantity_available = models.IntegerField()
    quantity_checked_out = models.IntegerField(default=0)

    class Meta:
        managed = False
        db_table = 'resources'

    def __str__(self):
        return (str(self.isbn) + ', ' + str(self.library))


class Author(models.Model):
    author_id = models.AutoField(primary_key=True)
    author_name = models.CharField(unique=True, max_length=255)

    class Meta:
        managed = False
        db_table = 'authors'

    def __str__(self):
        return self.author_name


class BookAuthor(models.Model):
    author = models.OneToOneField(Author, models.CASCADE, primary_key=True)  # The composite primary key (author_id, isbn) found, that is not supported. The first column is selected.
    isbn = models.ForeignKey(Book, models.CASCADE, db_column='isbn')

    class Meta:
        managed = False
        db_table = 'books_authors'
        unique_together = (('author', 'isbn'),)

    def __str__(self):
        return (str(self.author) + ', ' + str(self.isbn))


class Rental(models.Model):
    rental_id = models.AutoField(primary_key=True)
    member = models.ForeignKey(Member, models.PROTECT)
    library = models.ForeignKey(Library, models.PROTECT)
    rental_date = models.DateField()
    rental_status = models.CharField(max_length=7)

    class Meta:
        managed = False
        db_table = 'rentals'


class RentalItem(models.Model):
    rental = models.OneToOneField(Rental, models.CASCADE, primary_key=True)  # The composite primary key (rental_id, resource_id) found, that is not supported. The first column is selected.
    resource = models.ForeignKey(Resource, models.CASCADE)
    queue_num = models.IntegerField()
    rental_item_status = models.CharField(max_length=255)
    return_date = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'rental_items'
        unique_together = (('rental', 'resource'),)

    def __str__(self):
        return (str(self.resource) + ', ' + self.rental_item_status)
