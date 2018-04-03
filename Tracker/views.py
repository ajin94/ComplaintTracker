from django.shortcuts import render, redirect, reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import TrackerMaster, TrackerStatus
from .forms import NewComplaintForm
# Create your views here.


class Constants:
    processing = 'processing'


def main_tracker(request):

    if request.method == 'POST':
        input_data = NewComplaintForm(request.POST)
        if input_data.is_valid():
            input_data_stream = input_data.save(commit=False)
            input_data_stream.complaint_status = TrackerStatus.objects.get(name=Constants.processing).id
            input_data_stream.save()
        else:
            print("error")
            print(input_data)
        return reverse('main_tracker')
    else:
        complaints_data = TrackerMaster.objects.all()
        if TrackerMaster.objects.count() > 20:
            paginator = Paginator(complaints_data, 20)
            page = request.GET.get('page', 1)
            complaints_data = paginator.get_page(page)

    return render(request, 'Tracker/index.html', {"page_name": "tracker_home", "login_status": True,
                                                  "complaint_list": complaints_data, 'new_complaint': NewComplaintForm})
