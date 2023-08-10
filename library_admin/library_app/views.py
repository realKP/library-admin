from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import generic, View
from django.template import RequestContext
from django.db.models import Count
from .forms import MemberForm, ResourceForm, BookForm
from .models import Member, Library, Book, Author, Resource, Rental, RentalItem, BookAuthor


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
        context["saved"] = False

        # alert for update status
        status = self.request.GET.dict().get("saved")
        if status == "Error":
            context["saved"] = "Error"
        elif status:
            context["saved"] = True
        else:
            context["saved"] = False
        return context

    def post(self, request, *args, **kwargs):
        form = MemberForm(request.POST)
        if form.is_valid():
            # process the data in form.cleaned_data as required
            form.save()
            # redirect to members page to display new entry
            return HttpResponseRedirect(reverse("library_app:members") + '?saved=True')
        else:
            return render(request, "library_app/members.html", {"members": self.queryset, "form": form, "saved": "Error"})


class DeleteMember(View):
    http_method_names = ['delete']

    def dispatch(self, *args, **kwargs):
        method = self.request.POST.get('_method', '').lower()
        if method == 'delete':
            return self.delete(*args, **kwargs)
        else:
            return super(DeleteMember, self).dispatch(*args, **kwargs)

    def delete(self, request, *args, **kwargs):
        member = get_object_or_404(Member, pk=kwargs['pk'])
        member.delete()
        return HttpResponseRedirect(reverse("library_app:members"))


class MemberView(generic.DetailView):
    model = Member
    template_name = "library_app/member.html"
    context_object_name = "member"

    def dispatch(self, *args, **kwargs):
        method = self.request.POST.get('_method', '').lower()
        if method == 'patch':
            return self.patch(*args, **kwargs)
        else:
            return super(MemberView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        # every request receives prefilled form to display
        context = super().get_context_data(**kwargs)
        form = MemberForm(instance=self.object)
        context["form"] = form
        context["saved"] = False

        # alert for update status
        status = self.request.GET.dict().get("saved")
        if status == "Error":
            context["saved"] = "Error"
        elif status:
            context["saved"] = True
        else:
            context["saved"] = False

        # member's rental history
        context["rentals"] = Rental.objects.filter(member_id=kwargs['object'].member_id).order_by("-rental_date").select_related("library").annotate(Count("rentalitem"))
        return context

    def patch(self, request, *args, **kwargs):
        member = self.get_object()
        form = MemberForm(request.POST, instance=self.get_object())
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("library_app:member", args=[member.member_id]) + '?saved=True')
        else:
            return render(request, "library_app/member.html", {"member": member, "form": form, "saved": "Error"})


class EditMember(View):
    http_method_names = ['patch']

    def dispatch(self, *args, **kwargs):
        method = self.request.POST.get('_method', '').lower()
        if method == 'patch':
            return self.patch(*args, **kwargs)
        else:
            return super(EditMember, self).dispatch(*args, **kwargs)

    def patch(self, request, *args, **kwargs):
        member = self.get_object()
        form = MemberForm(request.POST, instance=self.get_object())
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("library_app:member", args=[member.member_id]) + '?saved=True')
        else:
            return HttpResponseRedirect(reverse("library_app:member", args=[member.member_id]) + '?saved=Error')


class LibrariesView(generic.ListView):
    template_name = "library_app/libraries.html"
    context_object_name = "libraries"
    # queries for all libraries
    queryset = Library.objects.all()


class LibraryView(generic.ListView):
    template_name = "library_app/library.html"
    context_object_name = "resources"

    def get_queryset(self):
        context = []
        resources = Resource.objects.filter(library_id=self.kwargs['pk']).order_by("resource_id").select_related("isbn")
        for resource in resources:
            info = {}
            info["resource_id"] = resource.resource_id
            info["isbn"] = resource.isbn.isbn
            info["book_title"] = resource.isbn.book_title
            info["quantity_available"] = resource.quantity_available
            info["quantity_checked_out"] = resource.quantity_checked_out
            books_authors = BookAuthor.objects.filter(isbn=resource.isbn.isbn).select_related("author")
            authors_list = []
            for book_author in books_authors:
                authors_list.append(book_author.author.author_name)
            info["authors"] = ", ".join(authors_list)
            context.append(info)
        return context

    def get_context_data(self, **kwargs):
        # library info to display at top of page
        context = super().get_context_data(**kwargs)
        library = get_object_or_404(Library, pk=self.kwargs['pk'])
        context["library"] = library

        context["rentals"] = Rental.objects.filter(library_id=self.kwargs['pk']).order_by("-rental_date").annotate(Count("rentalitem"))
        return context


class RentalItemsView(generic.ListView):
    template_name = "library_app/rental-items.html"
    context_object_name = "rental_items"

    def get_queryset(self):
        return RentalItem.objects.filter(rental_id=self.kwargs['pk']).select_related("resource", "resource__isbn")


class ResourcesView(generic.ListView):
    template_name = "library_app/resources.html"
    context_object_name = "resources"
    # queries for all members
    queryset = Resource.objects.all().select_related("isbn")

    def get_context_data(self, **kwargs):
        # every request (GET or POST) receives blank form for modal
        context = super().get_context_data(**kwargs)
        form = ResourceForm()
        context["form"] = form
        return context

    def post(self, request, *args, **kwargs):
        form = MemberForm(request.POST)
        if form.is_valid():
            # process the data in form.cleaned_data as required
            form.save()
            # redirect to members page to display new entry
            return HttpResponseRedirect(reverse("library_app:resources"))


class ResourceView(generic.DetailView):
    model = Resource
    template_name = "library_app/resource.html"
    context_object_name = "resource"

    def get_context_data(self, **kwargs):
        # every request receives prefilled form to display
        context = super().get_context_data(**kwargs)

        # member's rental history
        context["libraries"] = Library.objects.filter(library_id=kwargs['object'].library_id)
        return context


class BooksView(generic.ListView):
    template_name = "library_app/books.html"
    context_object_name = "books"
    # queries for all members
    queryset = Book.objects.all()

    def get_context_data(self, **kwargs):
        # every request (GET or POST) receives blank form for modal
        context = super().get_context_data(**kwargs)
        form = BookForm()
        context["form"] = form
        context["saved"] = False

        # alert for update status
        status = self.request.GET.dict().get("saved")
        if status == "Error":
            context["saved"] = "Error"
        elif status:
            context["saved"] = True
        else:
            context["saved"] = False
        return context

    def post(self, request, *args, **kwargs):
        form = BookForm(request.POST)
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # form.save()
            print(form)
            # redirect to members page to display new entry
            return HttpResponseRedirect(reverse("library_app:books") + '?saved=True')
        else:
            return render(request, "library_app/books.html", {"books": self.queryset, "form": form, "saved": "Error"})
