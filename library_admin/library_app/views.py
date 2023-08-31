from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic, View
from django.db.models import Count, F
from .forms import MemberForm, ResourceForm, EditResourceForm, \
    LibraryResourceForm, BookForm, LibraryRentalForm, RentalItemForm
from .models import Member, Library, Book, Author, Resource, Rental, \
    RentalItem, BookAuthor
from .utility_functions import clean_authors
from datetime import date, timedelta


def index(request):
    """
    Home page
    """
    return render(request, "library_app/index.html", {})


class MembersView(generic.ListView):
    """
    General members page
    """
    template_name = "library_app/members.html"
    context_object_name = "members"
    # queries for all members
    queryset = Member.objects.all()

    def get_context_data(self, **kwargs):
        # every request (GET or POST) receives blank form for modal
        context = super().get_context_data(**kwargs)
        form = MemberForm()
        context["form"] = form

        # flag for status banner
        context["saved"] = False
        status = self.request.GET.dict().get("saved")
        if status == "Error":
            context["saved"] = "Error"
        elif status:
            context["saved"] = True
        else:
            context["saved"] = False
        return context

    def post(self, request, *args, **kwargs):
        """
        Custom handler for POST requests
        """
        form = MemberForm(request.POST)
        if form.is_valid():
            form.save()
            # redirect to members page to display new member
            return HttpResponseRedirect(
                reverse("library_app:members") + '?saved=True'
            )
        else:
            return render(
                request,
                "library_app/members.html",
                {
                    "members": self.queryset,
                    "form": form,
                    "saved": "Error"
                }
            )


class DeleteMember(View):
    """
    Delete member functionality
    """
    http_method_names = ['delete']

    def dispatch(self, *args, **kwargs):
        """
        Custom request dispatcher
        """
        method = self.request.POST.get('_method', '').lower()
        if method == 'delete':
            return self.delete(*args, **kwargs)
        else:
            return super(DeleteMember, self).dispatch(*args, **kwargs)

    def delete(self, request, *args, **kwargs):
        """
        Custom handler for 'DELETE' requests
        """
        member = get_object_or_404(Member, pk=kwargs['pk'])
        member.delete()
        # redirect to members page
        return HttpResponseRedirect(reverse("library_app:members"))


class MemberView(generic.DetailView):
    """
    Individual member's page
    """
    model = Member
    template_name = "library_app/member.html"
    context_object_name = "member"

    def dispatch(self, *args, **kwargs):
        """
        Custom request dispatcher
        """
        method = self.request.POST.get('_method', '').lower()
        if method == 'patch':
            return self.patch(*args, **kwargs)
        else:
            return super(MemberView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        # every request (GET or POST) receives prefilled form
        context = super().get_context_data(**kwargs)
        form = MemberForm(instance=self.object)
        context["form"] = form

        # flag for status banner
        context["saved"] = False
        status = self.request.GET.dict().get("saved")
        if status == "Error":
            context["saved"] = "Error"
        elif status:
            context["saved"] = True
        else:
            context["saved"] = False

        # retrieves member's rental history
        context["rentals"] = Rental.objects.\
            filter(member_id=kwargs['object'].member_id).\
            order_by("-rental_date").\
            select_related("library").\
            annotate(Count("rentalitem"))   # how many items are in each rental
        return context

    def patch(self, request, *args, **kwargs):
        """
        Custom handler for 'PATCH' requests
        """
        member = self.get_object()
        form = MemberForm(request.POST, instance=member)
        if form.is_valid():
            form.save()
            # redirect to member page to display updated info
            return HttpResponseRedirect(
                reverse("library_app:member", args=[member.member_id]) + '?saved=True'
            )
        else:
            return render(
                request,
                "library_app/member.html",
                {
                    "member": member,
                    "form": form,
                    "saved": "Error"
                }
            )


class LibrariesView(generic.ListView):
    """
    General libraries page
    """
    template_name = "library_app/libraries.html"
    context_object_name = "libraries"
    # queries for all libraries
    queryset = Library.objects.all()


class LibraryView(generic.ListView):
    """
    Individual library's page
    """
    template_name = "library_app/library.html"
    context_object_name = "resources"

    def get_queryset(self):
        """
        Custom query for resources and related book/author info
        """
        context = []

        resources = Resource.objects.\
            filter(library_id=self.kwargs['pk']).\
            order_by("resource_id").\
            select_related("isbn")
        for resource in resources:
            info = {}
            info["resource_id"] = resource.resource_id
            info["isbn"] = resource.isbn.isbn
            info["book_title"] = resource.isbn.book_title
            info["quantity_available"] = resource.quantity_available
            info["quantity_checked_out"] = resource.quantity_checked_out
            info["queue_num"] = resource.queue_num

            books_authors = BookAuthor.objects.\
                filter(isbn=resource.isbn.isbn).\
                select_related("author")
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

        # rentals info
        context["rentals"] = Rental.objects.\
            filter(library_id=self.kwargs['pk']).\
            order_by("-rental_date").\
            annotate(Count("rentalitem")).\
            select_related("member")

        # forms info
        resource_form = LibraryResourceForm(
            initial={
                'library': self.kwargs['pk']
            }
        )
        context["resource_form"] = resource_form
        rental_form = LibraryRentalForm(
            info=self.get_queryset(),
            initial={
                'library': self.kwargs['pk'],
                'rental_date': date.today(),
                'rental_status': 'OPEN'
            }
        )
        context["rental_form"] = rental_form

        # flag for status banner
        context["saved"] = False
        status = self.request.GET.dict().get("saved")
        if status == "Error":
            context["saved"] = "Error"
        elif status:
            context["saved"] = True
        else:
            context["saved"] = False
        return context

    def post(self, request, *args, **kwargs):
        """
        Custom handler for POST requests
        """
        resource_form = LibraryResourceForm(request.POST)
        if resource_form.is_valid():
            resource_form.save()
            # redirect to library page to display new resource
            return HttpResponseRedirect(
                reverse("library_app:library", args=[self.kwargs['pk']]) + '?saved=True')
        else:
            rental_form = LibraryRentalForm(
                info=self.get_queryset(),
                initial={
                    'library': self.kwargs['pk'],
                    'rental_date': date.today(),
                    'rental_status': 'OPEN'
                }
            )
            library = get_object_or_404(Library, pk=self.kwargs['pk'])
            rentals = Rental.objects.\
                filter(library_id=self.kwargs['pk']).\
                order_by("-rental_date").\
                annotate(Count("rentalitem"))   # how many items are in each rental

            # need to repopulate forms if submission isn't valid
            return render(
                request,
                "library_app/library.html",
                {
                    "resources": self.get_queryset(),
                    "resource_form": resource_form,
                    "rental_form": rental_form,
                    "saved": "Error",
                    "library": library,
                    "rentals": rentals
                }
            )


class AddLibraryRental(View):
    """
    Add new rental on individual library's page
    """
    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        """
        Custom handler for POST requests
        """
        resources = Resource.objects.\
            filter(library_id=self.kwargs['pk']).\
            order_by("resource_id").\
            select_related("isbn")

        rental_form = LibraryRentalForm(request.POST, info=resources)
        if rental_form.is_valid():
            # create rental
            new_rental = rental_form.save()

            # create rental items
            isbns = request.POST.getlist('resources')
            for isbn in isbns:
                resource = get_object_or_404(
                    Resource,
                    isbn=isbn,
                    library=rental_form.cleaned_data['library']
                )
                # resource is available
                if resource.quantity_available > 0:
                    resource.quantity_available = F("quantity_available") - 1
                    resource.quantity_checked_out = F("quantity_checked_out") + 1
                    resource.save()
                    status = "CHECKED OUT"
                    return_date = date.today() + timedelta(days=14)
                    queue_pos = 0
                # resource unavailable, add to waitlist (queue)
                else:
                    status = "RESERVED"
                    queue_pos = resource.queue_num + 1
                    resource.queue_num = F("queue_num") + 1
                    resource.save()
                    return_date = None

                rental_item = RentalItem(
                    rental=new_rental,
                    resource=resource,
                    rental_item_status=status,
                    return_date=return_date,
                    queue_pos=queue_pos
                )
                rental_item.save()

            # redirect to library page to display new rental
            return HttpResponseRedirect(reverse("library_app:library", args=[self.kwargs['pk']]) + '?saved=True')
        else:
            resource_form = LibraryResourceForm(
                initial={
                    'library': self.kwargs['pk']
                }
            )
            library = get_object_or_404(Library, pk=self.kwargs['pk'])
            rentals = Rental.objects.\
                filter(library_id=self.kwargs['pk']).\
                order_by("-rental_date").\
                annotate(Count("rentalitem"))

            # need to repopulate forms if submission isn't valid
            return render(
                request,
                "library_app/library.html",
                {
                    "resources": resources,
                    "rental_form": rental_form,
                    "resource_form": resource_form,
                    "saved": "Error",
                    "library": library,
                    "rentals": rentals
                }
            )


class RentalItemsView(generic.ListView):
    """
    Rental Items for individual Rental's page
    """
    template_name = "library_app/rental-items.html"
    context_object_name = "rental_items"

    def get_queryset(self):
        """
        Custom query for rental items and related members, resources, and books
        """
        return RentalItem.objects.\
            filter(rental_id=self.kwargs['pk']).\
            select_related("rental", "rental__member", "resource", "resource__isbn")

    def get_context_data(self, **kwargs):
        # rental info to display at top of page
        context = super().get_context_data(**kwargs)
        context["rental"] = self.get_queryset()[0].rental
        return context


class RentalItemView(generic.ListView):
    """
    Individual rental item page
    """
    model = RentalItem
    template_name = "library_app/rental-item.html"
    context_object_name = "rental_item"

    def dispatch(self, *args, **kwargs):
        """
        Custom request dispatcher
        """
        method = self.request.POST.get('_method', '').lower()
        if method == 'patch':
            return self.patch(*args, **kwargs)
        else:
            return super(RentalItemView, self).dispatch(*args, **kwargs)

    def get_queryset(self):
        """
        Custom query for rental item and related resource and book
        """
        rental_item = RentalItem.objects.\
            filter(rental_id=self.kwargs['rental'], resource_id=self.kwargs['resource']).\
            select_related("rental", "resource", "resource__isbn")
        return rental_item[0]

    def get_context_data(self, **kwargs):
        # every request receives prefilled form to display
        context = super().get_context_data(**kwargs)
        form = RentalItemForm(instance=self.get_queryset())
        context["form"] = form

        # flag for status banner
        context["saved"] = False
        status = self.request.GET.dict().get("saved")
        if status == "Error":
            context["saved"] = "Error"
        elif status:
            context["saved"] = True
        else:
            context["saved"] = False
        return context

    def patch(self, request, *args, **kwargs):
        """
        Custom handler for 'PATCH' requests
        """
        rental_item = self.get_queryset()
        form = RentalItemForm(request.POST, instance=rental_item)
        if form.is_valid():
            form.save()
            # redirect to rental item page to display updated info
            return HttpResponseRedirect(
                reverse("library_app:rental-item", args=[self.kwargs['rental'], self.kwargs['resource']]) + '?saved=True'
            )
        else:
            return render(
                request,
                "library_app/rental-item.html",
                {
                    "rental_item": rental_item,
                    "form": form,
                    "saved": "Error"
                }
            )


class ResourcesView(generic.ListView):
    """
    General resources page
    """
    template_name = "library_app/resources.html"
    context_object_name = "resources"
    # queries for all resources
    queryset = Resource.objects.all().select_related("isbn")

    def get_context_data(self, **kwargs):
        # every request (GET or POST) receives blank form for modal
        context = super().get_context_data(**kwargs)
        form = ResourceForm()
        context["form"] = form

        # flag for status banner
        context["saved"] = False
        status = self.request.GET.dict().get("saved")
        if status == "Error":
            context["saved"] = "Error"
        elif status:
            context["saved"] = True
        else:
            context["saved"] = False
        return context

    def post(self, request, *args, **kwargs):
        """
        Custom handler for POST requests
        """
        form = ResourceForm(request.POST)
        if form.is_valid():
            form.save()
            # redirect to resources page to display new resource
            return HttpResponseRedirect(
                reverse("library_app:resources") + '?saved=True'
            )
        else:
            return render(
                request,
                "library_app/resources.html",
                {
                    "resources": self.get_queryset(),
                    "form": form,
                    "saved": "Error"
                }
            )


class ResourceView(generic.DetailView):
    """
    Individual resource page
    """
    model = Resource
    template_name = "library_app/resource.html"
    context_object_name = "resource"

    def dispatch(self, *args, **kwargs):
        """
        Custom request dispatcher
        """
        method = self.request.POST.get('_method', '').lower()
        if method == 'patch':
            return self.patch(*args, **kwargs)
        else:
            return super(ResourceView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        # every request (GET or POST) receives prefilled form
        context = super().get_context_data(**kwargs)
        form = EditResourceForm(instance=self.object)
        context["form"] = form

        # flag for status banner
        context["saved"] = False
        status = self.request.GET.dict().get("saved")
        if status == "Error":
            context["saved"] = "Error"
        elif status:
            context["saved"] = True
        else:
            context["saved"] = False

        return context

    def patch(self, request, *args, **kwargs):
        """
        Custom handler for 'PATCH' requests
        """
        resource = self.get_object()
        form = EditResourceForm(request.POST, instance=resource)
        if form.is_valid():
            form.save()
            # redirect to resource page to display updated info
            return HttpResponseRedirect(
                reverse("library_app:resource", args=[resource.resource_id]) + '?saved=True'
            )
        else:
            return render(
                request,
                "library_app/resource.html",
                {
                    "resource": resource,
                    "form": form,
                    "saved": "Error"
                }
            )


class BooksView(generic.ListView):
    """
    General books page
    """
    template_name = "library_app/books.html"
    context_object_name = "books"

    def get_queryset(self):
        """
        Custom query for books and related resource and author info
        """
        context = []
        books = Book.objects.all()
        for book in books:
            info = {}
            info["isbn"] = book.isbn
            info["book_title"] = book.book_title
            books_authors = BookAuthor.objects.\
                filter(isbn=book.isbn).\
                select_related("author")
            authors_list = []
            for book_author in books_authors:
                authors_list.append(book_author.author.author_name)
            info["authors"] = ", ".join(authors_list)
            context.append(info)
            info["resources"] = Resource.objects.\
                filter(isbn=book.isbn).\
                select_related("library")
        return context

    def get_context_data(self, **kwargs):
        # every request (GET or POST) receives blank form for modal
        context = super().get_context_data(**kwargs)
        form = BookForm()
        context["form"] = form

        # flag for status banner
        context["saved"] = False
        status = self.request.GET.dict().get("saved")
        if status == "Error":
            context["saved"] = "Error"
        elif status:
            context["saved"] = True
        else:
            context["saved"] = False
        return context

    def post(self, request, *args, **kwargs):
        """
        Custom handler for POST requests
        """
        form = BookForm(request.POST)
        if form.is_valid():
            # create book
            form.save()
            # creates authors and books_authors
            authors = clean_authors(request.POST["authors"])
            book = get_object_or_404(Book, pk=form.cleaned_data["isbn"])
            for name in authors:
                # check if author exists; if not, create author
                author, created = Author.objects.get_or_create(author_name=name)
                # create book_author
                ba = BookAuthor.objects.create(author=author, isbn=book)

            # redirect to books page to display new book
            return HttpResponseRedirect(reverse("library_app:books") + '?saved=True')
        else:
            return render(
                request,
                "library_app/books.html",
                {
                    "books": self.get_queryset(),
                    "form": form,
                    "saved": "Error"
                }
            )
