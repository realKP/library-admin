from django.db import models

RENTAL_STATUS_CHOICES = [
    ("OPEN", "OPEN"),
    ("CLOSED", "CLOSED"),
    ("OVERDUE", "OVERDUE")
]

RENTAL_ITEM_STATUS_CHOICES = [
    ("CHECKED OUT", "CHECKED OUT"),
    ("RESERVED", "RESERVED"),
    ("OVERDUE", "OVERDUE"),
    ("RETURNED", "RETURNED")
]


class Member(models.Model):
    member_id = models.AutoField(primary_key=True)
    member_first_name = models.CharField(max_length=255)
    member_last_name = models.CharField(max_length=255)
    member_phone = models.CharField(max_length=10)
    member_email = models.EmailField(max_length=255)

    class Meta:
        managed = False
        db_table = 'members'
        unique_together = (
            ('member_first_name',
             'member_last_name',
             'member_email'),
        )

    def __str__(self):
        return (self.member_first_name + ' ' + self.member_last_name)


class Book(models.Model):
    isbn = models.CharField(primary_key=True, max_length=13)
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
    queue_num = models.IntegerField(default=0)

    class Meta:
        managed = False
        db_table = 'resources'
        unique_together = (('isbn', 'library'),)

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
    author = models.OneToOneField(Author, models.CASCADE, primary_key=True)
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
    rental_status = models.CharField(
        max_length=7,
        choices=RENTAL_STATUS_CHOICES
    )

    class Meta:
        managed = False
        db_table = 'rentals'


class RentalItem(models.Model):
    rental_item_id = models.CharField(primary_key=True, max_length=255)
    rental = models.ForeignKey(Rental, models.CASCADE)
    resource = models.ForeignKey(Resource, models.CASCADE)
    rental_item_status = models.CharField(
        max_length=11,
        choices=RENTAL_ITEM_STATUS_CHOICES
    )
    return_date = models.DateField(blank=True, null=True)
    queue_pos = models.IntegerField(default=0)

    class Meta:
        managed = False
        db_table = 'rental_items'

    def __str__(self):
        return (str(self.resource) + ', ' + self.rental_item_status)
