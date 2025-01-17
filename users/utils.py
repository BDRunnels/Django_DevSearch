from .models import Profile, Skill
from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

def paginate_profiles(request, profiles):

    page = request.GET.get("page")
    results = 3
    paginator = Paginator(profiles, results)
    
    try:
        profiles = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        profiles = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        profiles = paginator.page(page)

    left_index = (int(page) - 4)

    if left_index < 1:
        left_index = 1
    
    right_index = (int(page) + 5)

    if right_index > paginator.num_pages:
        right_index = paginator.num_pages

    custom_range = range(left_index, right_index + 1)
    return custom_range, profiles


def search_profiles(request):
    search_query = ""
     
    if request.GET.get('search_query'):
        search_query = request.GET.get("search_query")

    skills = Skill.objects.filter(skill_name__icontains=search_query)
    print("SEARCH:", search_query)

    profiles = Profile.objects.distinct().filter(Q(name__icontains=search_query) | 
                                      Q(short_intro__icontains=search_query) |
                                      Q(skill__in=skills)
                                      )

    return profiles, search_query
