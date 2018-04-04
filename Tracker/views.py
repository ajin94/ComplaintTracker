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
            input_data_stream.complaint_status = TrackerStatus.objects.get(name=Constants.processing)
            input_data_stream.save()

        else:
            print("error")
        return redirect('main_tracker')
    else:
        complaints_data = TrackerMaster.objects.all()
        if TrackerMaster.objects.count() > 10:
            paginator = Paginator(complaints_data, 10)
            page = request.GET.get('page', 1)
            try:
                complaints_data = paginator.get_page(page)
            except EmptyPage:
                complaints_data = paginator.get_page(paginator.num_pages, orphans=TrackerMaster.objects.count() % 10)
    return render(request, 'Tracker/index.html',
                  {"page_name": "tracker_home",
                   "login_status": True,
                   "complaint_list": complaints_data,
                   'new_complaint': NewComplaintForm,
                   }
                  )
