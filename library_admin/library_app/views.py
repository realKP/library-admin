from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from .forms import MemberForm
from .models import Member, Library, Book, Author, Resource, Rental, RentalItem, BookAuthor

# Create your views here.


def index(request):
    return render(request, "library_app/index.html", {})


class MembersView(generic.ListView):
    template_name = "library_app/members.html"
    context_object_name = "members"
    queryset = Member.objects.all()


def get_member_info(request):
    # if this is a POST request we need to process the form data
    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        form = MemberForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            form.save()
            # redirect to a new URL:
            return HttpResponseRedirect("/members/")

    # if a GET (or any other method) we'll create a blank form
    else:
        form = MemberForm()
    context = {"add-member-form": form}
    return render(request, "library_app/add-member.html", context)

##########################################################
def member(request):
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
