from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib import messages
from .models import Project, Tag
from .forms import ProjectForm, ReviewForm
from .utils import search_projects, paginate_projects
# Create your views here.


def get_projects(request):
    projects_list, search_query = search_projects(request)

    custom_range, projects_list = paginate_projects(request, projects_list)

    context = {"projects": projects_list, "search_query": search_query, "custom_range": custom_range}
    return render(request, "projects/projects.html", context)


def get_single_project(request, primary_key):   # 2nd parameter must match str: in path.
    project_obj = Project.objects.get(id=primary_key)
    form = ReviewForm()

    if request.method == "POST":
        form = ReviewForm(request.POST)
        review = form.save(commit=False)
        review.project = project_obj
        review.owner = request.user.profile
        review.save()

        #Update project votecount
        messages.success(request, "Your review was successfully submitted")
        return redirect("project", primary_key=project_obj.id)
    
    return render(request, "projects/single-project.html", {"project": project_obj, "form": form})


def get_home_page(request):
    return HttpResponse("Home Page")


@login_required(login_url="login")
def create_project(request):
    profile = request.user.profile
    form = ProjectForm()

    if request.method == "POST":
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = profile
            project.save()
            return redirect("account")

    context = {"form": form}

    return render(request, "projects/project_form.html", context)


@login_required(login_url="login")
def update_project(request, primary_key):
    profile = request.user.profile
    project_to_update = profile.project_set.get(id=primary_key)
    form = ProjectForm(instance=project_to_update)

    if request.method == "POST":
        form = ProjectForm(request.POST, request.FILES, instance=project_to_update)
        if form.is_valid():
            form.save()
            return redirect("account")

    context = {"form": form}

    return render(request, "projects/project_form.html", context)


@login_required(login_url="login")
def delete_project(request, primary_key):
    profile = request.user.profile
    project_to_delete = profile.project_set.get(id=primary_key)

    if request.method == "POST":
        project_to_delete.delete()
        return redirect("projects")
    
    context = {"object": project_to_delete}

    return render(request, "delete_template.html", context)