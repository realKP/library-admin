# Generated by Django 4.2.3 on 2023-07-21 02:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('library_app', '0002_member_delete_members'),
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('author_id', models.AutoField(primary_key=True, serialize=False)),
                ('author_name', models.CharField(max_length=255, unique=True)),
            ],
            options={
                'db_table': 'authors',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('isbn', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('book_title', models.CharField(max_length=255, unique=True)),
            ],
            options={
                'db_table': 'books',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Library',
            fields=[
                ('library_id', models.AutoField(primary_key=True, serialize=False)),
                ('library_name', models.CharField(max_length=255, unique=True)),
                ('library_address', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'libraries',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Rental',
            fields=[
                ('rental_id', models.AutoField(primary_key=True, serialize=False)),
                ('rental_date', models.DateField()),
            ],
            options={
                'db_table': 'rentals',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Resource',
            fields=[
                ('resource_id', models.AutoField(primary_key=True, serialize=False)),
                ('quantity_available', models.IntegerField()),
                ('quanitity_checked_out', models.IntegerField()),
            ],
            options={
                'db_table': 'resources',
                'managed': False,
            },
        ),
        migrations.DeleteModel(
            name='Books',
        ),
        migrations.RemoveField(
            model_name='booksauthors',
            name='author',
        ),
        migrations.DeleteModel(
            name='Libraries',
        ),
        migrations.RemoveField(
            model_name='rentalitems',
            name='rental',
        ),
        migrations.DeleteModel(
            name='Resources',
        ),
        migrations.CreateModel(
            name='BookAuthor',
            fields=[
                ('author', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='library_app.author')),
            ],
            options={
                'db_table': 'books_authors',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='RentalItem',
            fields=[
                ('rental', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='library_app.rental')),
                ('queue_num', models.IntegerField()),
                ('rental_item_status', models.CharField(max_length=255)),
                ('return_date', models.DateField(blank=True, null=True)),
            ],
            options={
                'db_table': 'rental_items',
                'managed': False,
            },
        ),
        migrations.DeleteModel(
            name='Authors',
        ),
        migrations.DeleteModel(
            name='BooksAuthors',
        ),
        migrations.DeleteModel(
            name='RentalItems',
        ),
        migrations.DeleteModel(
            name='Rentals',
        ),
    ]
