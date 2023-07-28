from django.urls import path
from . import views

app_name = "library_app"
urlpatterns = [
    # home page
    path("", views.index, name="index"),
    # members page
    path("members/", views.MembersView.as_view(), name="members"),
    # add member
    # path("members/add_member", views.get_member_info, name="add-member"),
    # ex: /9781594133299
    # path("<str:isbn>/", views.detail, name="detail"),
    # # ex:
    # path("<int:question_id>/results/", views.results, name="results"),
    # # ex:
    # path("<int:question_id>/vote/", views.vote, name="vote"),
]
