from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User # django builtin user model
from .models import Profile
from .forms import CustomUserCreationForm, ProfileForm, SkillForm
from .utils import search_profiles, paginate_profiles

# Create your views here.

def profiles(request):
    profiles, search_query = search_profiles(request)

    custom_range, profiles = paginate_profiles(request, profiles)
    
    context = {"profiles": profiles, "search_query": search_query, "custom_range": custom_range}
    return render(request, "users/profiles.html", context)


def user_profile(request, primary_key):
    profile = Profile.objects.get(id=primary_key)
    print(profile)
    top_skills = profile.skill_set.exclude(skill_description__exact="")
    other_skills = profile.skill_set.filter(skill_description="")
    context = {
        "profile": profile,
        "top_skills": top_skills,
        "other_skills": other_skills,
    }
    return render(request, "users/user-profile.html", context)

@login_required(login_url="login")
def user_account(request):
    profile = request.user.profile

    skills = profile.skill_set.all()
    projects = profile.project_set.all()
    context = {"profile": profile, "skills": skills, "projects": projects}
    return render(request, "users/account.html", context)


@login_required(login_url="login")
def edit_account(request):
    profile = request.user.profile
    form = ProfileForm(instance=profile)

    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect("account")
        
    context = {"form": form}
    return render(request, "users/profile-form.html", context)


def login_user(request):
    page = "login"

    if request.user.is_authenticated:
        return redirect("profiles")
    
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        try:
            user = User.objects.get(username=username)
        except:
             messages.error(request, "Username does not exist")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("profiles")
        else:
            messages.error(request, "Username OR password is incorrect")

    return render(request, "users/login_register.html")


def logout_user(request):
    logout(request)
    messages.success(request, "Logout Success")

    return redirect("login")


def register_user(request):
    page = "register"
    form = CustomUserCreationForm()

    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            # lowercase username to prevent duplicates
            user_instance = form.save(commit=False)
            user_instance.username = user_instance.username.lower()
            user_instance.save()
            
            messages.success(request, f"{user_instance.username} successfully created")

            login(request, user_instance)
            return redirect("edit-account")
        else:
            messages.error(request, "An error occurred during sign up")
            
    context = {"page": page, "form": form}
    return render(request, "users/login_register.html", context)


@login_required(login_url='login')
def create_skill(request):
    profile = request.user.profile
    form = SkillForm()

    if request.method == "POST":
        form = SkillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.owner = profile
            skill.save()
            messages.success(request, f"{skill.skill_name} successfully added")
            return redirect("account")
        
    context = {"form": form}
    return render(request, "users/skill_form.html", context)


@login_required(login_url='login')
def update_skill(request, primary_key):
    profile = request.user.profile
    skill = profile.skill_set.get(id=primary_key)
    form = SkillForm(instance=skill)

    if request.method == "POST":
        form = SkillForm(request.POST, instance=skill)
        if form.is_valid():
            form.save()
            messages.success(request, f"{skill.skill_name} successfully updated")
            return redirect("account")
        
    context = {"form": form}
    return render(request, "users/skill_form.html", context)


@login_required(login_url='login')
def delete_skill(request, primary_key):
    profile = request.user.profile
    skill = profile.skill_set.get(id=primary_key)

    if request.method == "POST":
        skill.delete()
        messages.success(request, f"{skill.skill_name} successfully deleted")
        return redirect('account')
    
    context = {"object": skill}
    return render(request, 'delete_template.html', context)