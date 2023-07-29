from django import forms
from library_app.models import Member


class MemberForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ["member_first_name", "member_last_name", "member_phone", "member_email"]


# class EditMemberForm(MemberForm):
#     def __init__(self, *args, **kwargs):
#         super(MemberForm, self).__init__(*args, **kwargs)

#     class Meta:
#         model = Member
#         fields = ["member_phone", "member_email"]
