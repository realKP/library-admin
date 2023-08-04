from django.urls import path
from . import views

app_name = "library_app"
urlpatterns = [
    # home page
    path("", views.index, name="index"),
    # members page
    path("members/", views.MembersView.as_view(), name="members"),
    # delete member
    path("members/<int:pk>/", views.DeleteMember.as_view(), name="delete-member"),
    # edit member page
    path("members/<int:pk>/edit", views.EditMemberView.as_view(), name="edit-member"),
    # rental items page
    path("rentals/<int:pk>", views.RentalItemsView.as_view(), name="rental-items"),
    # libraries page
    path("libraries/", views.LibrariesView.as_view(), name="libraries"),
    # view a library's resources page
    path("libraries/<int:pk>/resources", views.LibraryResourcesView.as_view(), name="library-resources")


    ##########################################################3
    # ex: /9781594133299
    # path("<str:isbn>/", views.detail, name="detail"),
    # # ex:
    # path("<int:question_id>/results/", views.results, name="results"),
    # # ex:
    # path("<int:question_id>/vote/", views.vote, name="vote"),
]
