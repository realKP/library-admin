from django.db.models import Count, Q
from .models import Rental, RentalItem
from datetime import date


def clean_authors(authors: str):
    """
    Returns list of author names stripped of whitespace and capitalized
    """
    authors_raw = authors.split(";")
    authors_clean = [
        author.strip().title() for author in authors_raw if len(author.strip()) > 0
    ]
    return authors_clean


def update_rental_item_status(id: int, filter: str = None):
    """
    Updates statuses of past due rental items.
    Returns the number of objects matched (not objects
    updated since objects may already have status updated).
    """
    if filter == "library":
        rental_items = RentalItem.objects.\
            filter(rental__library_id=id, return_date__lt=date.today())
    elif filter == "member":
        rental_items = RentalItem.objects.\
            filter(rental__member_id=id, return_date__lt=date.today())
    else:
        rental_items = RentalItem.objects.\
            filter(rental_id=id, return_date__lt=date.today())

    return rental_items.update(rental_item_status="OVERDUE")


def update_rental_status(id: int, filter: str):
    """
    Returns queryset containing rentals with updated statuses based on
    their rental items statuses
    """
    # updates statuses of past due rental items
    update_rental_item_status(id, filter)

    # queryset of rentals with counts of each item statuses
    if filter == "library":
        rentals = Rental.objects.\
            filter(library_id=id).\
            order_by("-rental_date").\
            annotate(
                rentalitem__count=Count(
                    "rentalitem",
                    distinct=True
                )
            ).\
            annotate(
                rentalitem__overdue=Count(
                    "rentalitem",
                    distinct=True,
                    filter=Q(rentalitem__rental_item_status="OVERDUE")
                ),
            ).\
            annotate(
                rentalitem__closed=Count(
                    "rentalitem",
                    distinct=True,
                    filter=Q(rentalitem__rental_item_status="RETURNED")
                ),
            ).\
            select_related("member")
    elif filter == "member":
        rentals = Rental.objects.\
            filter(member_id=id).\
            order_by("-rental_date").\
            annotate(
                rentalitem__count=Count(
                    "rentalitem",
                    distinct=True
                )
            ).\
            annotate(
                rentalitem__overdue=Count(
                    "rentalitem",
                    distinct=True,
                    filter=Q(rentalitem__rental_item_status="OVERDUE")
                ),
            ).\
            annotate(
                rentalitem__closed=Count(
                    "rentalitem",
                    distinct=True,
                    filter=Q(rentalitem__rental_item_status="RETURNED")
                ),
            ).\
            select_related("library")
    else:
        rentals = []

    # updates rental status based on items' statuses
    for rental in rentals:
        if rental.rentalitem__overdue > 0:
            rental.rental_status = "OVERDUE"
        elif rental.rentalitem__count == rental.rentalitem__closed:
            rental.rental_status = "CLOSED"
        else:
            rental.rental_status = "OPEN"
        rental.save()

    return rentals
