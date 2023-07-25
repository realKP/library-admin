from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from .models import Member, Library, Book, Author, Resource, Rental, RentalItem, BookAuthor

# Create your views here.


def index(request):
    latest_book_list = Book.objects.order_by("-isbn")[:5]
    context = {
        "latest_book_list": latest_book_list,
    }
    return render(request, "library_app/index.html", context)


def detail(request, isbn):
    book = get_object_or_404(Book, pk=isbn)
    return render(request, "library_app/detail.html", {"book": book})


def results(request, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)


def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)
