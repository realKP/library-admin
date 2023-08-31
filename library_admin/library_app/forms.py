from django import forms
from library_app.models import Member, Resource, Book, Rental, RentalItem
from django.utils.translation import gettext_lazy as _
from datetime import date, timedelta


class MemberForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = [
            "member_first_name",
            "member_last_name",
            "member_phone",
            "member_email"
        ]
        labels = {
            "member_first_name": _("First Name"),
            "member_last_name": _("Last Name"),
            "member_phone": _("Phone Number"),
            "member_email": _("Email")
        }
        help_texts = {
            "member_phone": _("No dashes, spaces, or parantheses. Example: 2344567890"),
        }
        widgets = {
            "member_first_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder":
                    "First Name",
                    "minlength": 2
                }
            ),
            "member_last_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Last Name",
                    "minlength": 2
                }
            ),
            "member_phone": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Phone",
                    "pattern": "[0-9]{10}",
                    "type": "tel"
                }
            ),
            "member_email": forms.EmailInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Email"
                }
            )
        }

    def clean_member_first_name(self):
        return self.cleaned_data["member_first_name"].title()

    def clean_member_last_name(self):
        return self.cleaned_data["member_last_name"].title()


class ResourceForm(forms.ModelForm):
    class Meta:
        model = Resource
        fields = ["isbn", "library", "quantity_available"]
        labels = {
            "isbn": _("Book Title"),
            "library": _("Library"),
            "quantity_available": _("QTY Available")
        }
        widgets = {
            "isbn": forms.Select(
                attrs={
                    "class": "form-control"
                }
            ),
            "library": forms.Select(
                attrs={
                    "class": "form-control"
                }
            ),
            "quantity_available": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": 1, "max": 100
                }
            )
        }

    def __init__(self, *args, **kwargs):
        super(ResourceForm, self).__init__(*args, **kwargs)

        # to display book titles as options in drop down menus
        books = Book.objects.all()
        book_choices = [(book.isbn, book.book_title) for book in books]
        self.fields['isbn'].choices = book_choices


class EditResourceForm(ResourceForm):
    def __init__(self, *args, **kwargs):
        super(ResourceForm, self).__init__(*args, **kwargs)

    class Meta(ResourceForm.Meta):
        fields = [
            "quantity_available"
        ]
        labels = {
            "quantity_available": _("QTY Available")
        }
        widgets = {
            "quantity_available": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": 0,
                    "max": 100
                }
            )
        }


class LibraryResourceForm(ResourceForm):
    class Meta(ResourceForm.Meta):
        widgets = {
            "isbn": forms.Select(
                attrs={
                    "class": "form-control"
                }
            ),
            "library": forms.HiddenInput(
                attrs={
                    "class": "form-control"
                }
            ),
            "quantity_available": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": 1,
                    "max": 100
                }
            )
        }


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ["isbn", "book_title"]
        labels = {
            "isbn": _("ISBN"),
            "book_title": _("Book Title")
        }
        help_texts = {
            "isbn": _("Only ISBN-13 format (no dashes) is accepted."),
        }
        widgets = {
            "isbn": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "ISBN",
                    "pattern": "[0-9]{13}"
                }
            ),
            "book_title": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Book Title",
                    "minlength": 2
                }
            ),
        }

    def clean_book_title(self):
        return self.cleaned_data["book_title"].title()


class RentalForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.info = kwargs.pop('info')  # list of dicts representing resources
        super(RentalForm, self).__init__(*args, **kwargs)

        # options for multiple selection widget
        try:
            resource_choices = [
                (resource['isbn'], resource['book_title']) for resource in self.info
            ]
        except TypeError:
            resource_choices = [
                (resource.isbn.isbn, resource.isbn.book_title) for resource in self.info
            ]

        # creates multiple select widget
        self.fields['resources'].widget = forms.CheckboxSelectMultiple(
            choices=resource_choices,
            attrs={"class": "form-control"}
        )
        self.fields['resources'].help_text = _("Select one or multiple resources to rent.")

    resources = forms.CharField()

    class Meta:
        model = Rental
        fields = ["member", "library", "rental_date", "rental_status"]
        labels = {
            "member": _("Member"),
            "library": _("Library"),
            "rental_date": _("Rental Date"),
            "rental_status": _("Rental Status")
        }
        widgets = {
            "member": forms.Select(
                attrs={
                    "class": "form-control"
                }
            ),
            "library": forms.Select(
                attrs={
                    "class": "form-control"
                }
            ),
            "rental_date": forms.DateInput(
                attrs={
                    "class": "form-control",
                    "type": "date",
                    "max": date.today(),
                    "min": "2023-01-01"
                }
            ),
            "rental_status": forms.Select(
                attrs={
                    "class": "form-control",
                    "maxlength": 7
                }
            ),
        }


class LibraryRentalForm(RentalForm):
    class Meta(RentalForm.Meta):
        widgets = {
            "member": forms.Select(
                attrs={
                    "class": "form-control"
                }
            ),
            "library": forms.HiddenInput(
                attrs={
                    "class": "form-control"
                }
            ),
            "rental_date": forms.DateInput(
                attrs={
                    "class": "form-control",
                    "type": "date",
                    "max": date.today(),
                    "min": "2023-01-01"
                }
            ),
            "rental_status": forms.HiddenInput(
                attrs={
                    "class": "form-control",
                    "maxlength": 7
                }
            )
        }


class RentalItemForm(forms.ModelForm):
    class Meta:
        model = RentalItem
        fields = ["return_date", "rental_item_status"]
        labels = {
            "return_date": _("Return Date"),
            "rental_item_status": _("Rental Item Status")
        }
        widgets = {
            "return_date": forms.DateInput(
                attrs={
                    "class": "form-control",
                    "type": "date",
                    "max": date.today() + timedelta(days=14),
                    "min": "2023-01-01"
                }
            ),
            "rental_item_status": forms.Select(
                attrs={
                    "class": "form-control"
                }
            )
        }
