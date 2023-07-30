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

##########################################################

# def results(request, question_id):
#     response = "You're looking at the results of question %s."
#     return HttpResponse(response % question_id)


# def vote(request, question_id):
#     return HttpResponse("You're voting on question %s." % question_id)
