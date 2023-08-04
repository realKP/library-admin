from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import generic, View
from django.template import RequestContext
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


class EditMemberView(generic.DetailView):
    http_method_names = ['get', 'patch']
    model = Member
    template_name = "library_app/edit-member.html"
    context_object_name = "member"

    def dispatch(self, *args, **kwargs):
        method = self.request.POST.get('_method', '').lower()
        if method == 'patch':
            return self.patch(*args, **kwargs)
        else:
            return super(EditMemberView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        # every request receives prefilled form to display
        context = super().get_context_data(**kwargs)
        form = MemberForm({
            "member_first_name": self.object.member_first_name,
            "member_last_name": self.object.member_last_name,
            "member_phone": self.object.member_phone,
            "member_email": self.object.member_email
        })
        context["form"] = form
        context["saved"] = False

        # alert for successful update
        if self.request.GET.dict().get("saved", False):
            context["saved"] = True

        # member's rental history
        context["rentals"] = Rental.objects.filter(member_id=kwargs['object'].member_id)
        resources = Resource.objects.all()
        for resource in resources:
            print(type(resource.isbn))
        return context

    def patch(self, request, *args, **kwargs):
        member = get_object_or_404(Member, pk=kwargs['pk'])
        payload = request.POST.dict()
        data_to_be_updated = {
            "member_first_name": payload["member_first_name"],
            "member_last_name": payload["member_last_name"],
            "member_phone": payload["member_phone"],
            "member_email": payload["member_email"]
        }
        for key, value in data_to_be_updated.items():
            setattr(member, key, value)
        member.save()
        return HttpResponseRedirect(reverse("library_app:edit-member", args=[member.member_id]) + '?saved=True')


class RentalItemsView(generic.DetailView):
    template_name = "library_app/rental-items.html"
    context_object_name = "rental_items"

    def get_queryset(self):
        return RentalItem.objects.filter(rental_id=self.kwargs['pk'])


class LibrariesView(generic.ListView):
    template_name = "library_app/libraries.html"
    context_object_name = "libraries"
    # queries for all libraries
    queryset = Library.objects.all()


class LibraryResourcesView(generic.ListView):
    template_name = "library_app/library-resources.html"
    context_object_name = "resources"

    def get_queryset(self):
        resources = Resource.objects.select_related("isbn").filter(library_id=self.kwargs['pk']).order_by("resource_id")
        context = []
        for resource in resources:
            info = {}
            info["resource_id"] = resource.resource_id
            info["isbn"] = resource.isbn.isbn
            info["book_title"] = resource.isbn.book_title
            info["quantity_available"] = resource.quantity_available
            info["quantity_checked_out"] = resource.quantity_checked_out
            books_authors = BookAuthor.objects.filter(isbn=resource.isbn)
            authors_list = []
            for book_author in books_authors:
                authors = Author.objects.filter(author_id=book_author.author_id)
                for author in authors:
                    authors_list.append(author.author_name)
            info["authors"] = ", ".join(authors_list)
            context.append(info)
        return context

    def get_context_data(self, **kwargs):
        # library info to display at top of page
        context = super().get_context_data(**kwargs)
        library = get_object_or_404(Library, pk=self.kwargs['pk'])
        context["library"] = library
        return context
