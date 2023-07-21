# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Members(models.Model):
    member_id = models.AutoField(primary_key=True)
    member_first_name = models.CharField(max_length=255)
    member_last_name = models.CharField(max_length=255)
    member_phone = models.CharField(max_length=15)
    member_email = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'members'


class Books(models.Model):
    isbn = models.CharField(primary_key=True, max_length=255)
    book_title = models.CharField(unique=True, max_length=255)

    class Meta:
        managed = False
        db_table = 'books'


class Libraries(models.Model):
    library_id = models.AutoField(primary_key=True)
    library_name = models.CharField(unique=True, max_length=255)
    library_address = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'libraries'


class Resources(models.Model):
    resource_id = models.AutoField(primary_key=True)
    isbn = models.ForeignKey(Books, models.PROTECT, db_column='isbn')
    library = models.ForeignKey(Libraries, models.PROTECT)
    quantity_available = models.IntegerField()
    quanitity_checked_out = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'resources'


class Authors(models.Model):
    author_id = models.AutoField(primary_key=True)
    author_name = models.CharField(unique=True, max_length=255)

    class Meta:
        managed = False
        db_table = 'authors'


class BooksAuthors(models.Model):
    author = models.OneToOneField(Authors, models.CASCADE, primary_key=True)  # The composite primary key (author_id, isbn) found, that is not supported. The first column is selected.
    isbn = models.ForeignKey(Books, models.CASCADE, db_column='isbn')

    class Meta:
        managed = False
        db_table = 'books_authors'
        unique_together = (('author', 'isbn'),)


class Rentals(models.Model):
    rental_id = models.AutoField(primary_key=True)
    member = models.ForeignKey(Members, models.PROTECT)
    library = models.ForeignKey(Libraries, models.PROTECT)
    rental_date = models.DateField()

    class Meta:
        managed = False
        db_table = 'rentals'


class RentalItems(models.Model):
    rental = models.OneToOneField(Rentals, models.CASCADE, primary_key=True)  # The composite primary key (rental_id, resource_id) found, that is not supported. The first column is selected.
    resource = models.ForeignKey('Resources', models.CASCADE)
    queue_num = models.IntegerField()
    rental_item_status = models.CharField(max_length=255)
    return_date = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'rental_items'
        unique_together = (('rental', 'resource'),)
