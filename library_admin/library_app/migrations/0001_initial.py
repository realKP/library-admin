# Generated by Django 4.2.3 on 2023-07-21 00:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Authors',
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
            name='Books',
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
            name='Libraries',
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
            name='Members',
            fields=[
                ('member_id', models.AutoField(primary_key=True, serialize=False)),
                ('member_first_name', models.CharField(max_length=255)),
                ('member_last_name', models.CharField(max_length=255)),
                ('member_phone', models.CharField(max_length=15)),
                ('member_email', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'members',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Rentals',
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
            name='Resources',
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
        migrations.CreateModel(
            name='BooksAuthors',
            fields=[
                ('author', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='library_app.authors')),
            ],
            options={
                'db_table': 'books_authors',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='RentalItems',
            fields=[
                ('rental', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='library_app.rentals')),
                ('queue_num', models.IntegerField()),
                ('rental_item_status', models.CharField(max_length=255)),
                ('return_date', models.DateField(blank=True, null=True)),
            ],
            options={
                'db_table': 'rental_items',
                'managed': False,
            },
        ),
    ]
