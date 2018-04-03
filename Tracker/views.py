from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import TrackerMaster
# Create your views here.


def main_tracker(request):

    complaints_data = TrackerMaster.objects.all()
    paginator = Paginator(complaints_data, 20)
    page = request.GET.get('page')

    complaints = paginator.get_page(page)
    return render(request, 'Tracker/index.html', {"page_name": "tracker_home", "login_status":True,
                                                  "complaints": complaints})
