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
    # queries for all members
    queryset = Member.objects.all()

    def get_context_data(self, **kwargs):
        # every request (GET or POST) receives blank form for modal
        context = super().get_context_data(**kwargs)
        form = MemberForm()
        context["form"] = form
        return context

    def post(self, request, *args, **kwargs):
        form = MemberForm(request.POST)
        if form.is_valid():
            # process the data in form.cleaned_data as required
            form.save()
            # redirect to members page to display new entry
            return HttpResponseRedirect(reverse("library_app:members"))


##########################################################

# def detail(request, isbn):
#     book = get_object_or_404(Book, pk=isbn)
#     return render(request, "library_app/detail.html", {"book": book})


# def results(request, question_id):
#     response = "You're looking at the results of question %s."
#     return HttpResponse(response % question_id)


# def vote(request, question_id):
#     return HttpResponse("You're voting on question %s." % question_id)
