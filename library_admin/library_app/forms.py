from django import forms
from library_app.models import Member, Resource
from crispy_forms.helper import FormHelper
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError


class MemberForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ["member_first_name", "member_last_name", "member_phone", "member_email"]
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
            "member_first_name": forms.TextInput(attrs={"class": "form-control", "placeholder": "First Name", "minlength": 2}),
            "member_last_name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Last Name", "minlength": 2}),
            "member_phone": forms.TextInput(attrs={"class": "form-control", "placeholder": "Phone", "pattern": "[0-9]{10}", "type": "tel"}),
            "member_email": forms.EmailInput(attrs={"class": "form-control", "placeholder": "Email"})
        }

    def clean_member_first_name(self):
        return self.cleaned_data["member_first_name"].title()

    def clean_member_last_name(self):
        return self.cleaned_data["member_last_name"].title()


class ResourceForm(forms.ModelForm):
    class Meta:
        model = Resource
        fields = ["isbn", "library", "quantity_available", "quantity_checked_out"]
