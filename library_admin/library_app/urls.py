from django.urls import path
from . import views

app_name = "library_app"
urlpatterns = [
    # home page
    path("", views.index, name="index"),
    # members page
    path("members/", views.MembersView.as_view(), name="members"),
    # view member page
    path("members/<int:pk>/", views.MemberView.as_view(), name="member"),
    # delete member
    path("members/<int:pk>/delete/", views.DeleteMember.as_view(), name="delete-member"),
    # edit member
    path("members/<int:pk>/edit/", views.EditMember.as_view(), name="edit-member"),
    # rental items page
    path("rentals/<int:pk>/", views.RentalItemsView.as_view(), name="rental-items"),
    # libraries page
    path("libraries/", views.LibrariesView.as_view(), name="libraries"),
    # view a library's resources page
    path("libraries/<int:pk>/resources/", views.LibraryResourcesView.as_view(), name="library-resources"),
    # resources page
    path("resources/", views.ResourcesView.as_view(), name="resources"),
    # resources page
    # path("resources/<int:pk>/", views.ResourceView.as_view(), name="resource"),
    # 
]
