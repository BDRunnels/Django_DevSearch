from django.urls import path
from . import views

urlpatterns = [
    path("", views.get_projects, name="projects"),
    path("project/<str:primary_key>/", views.get_single_project, name="project"),
    path("create-project/", views.create_project, name="create-project"),
    path("update-project/<str:primary_key>/", views.update_project, name="update-project"),
    path("delete-project/<str:primary_key>/", views.delete_project, name="delete-project"),
]