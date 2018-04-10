from django.shortcuts import render, redirect, reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import TrackerMaster, TrackerStatus
from django.contrib.auth.models import User
from .forms import NewComplaintForm, UserLoginForm
# Create your views here.


class Constants:
    processing = 'processing'


def main_tracker(request):
    # redirect login page if session not enabled
    if not request.session.get('user_department'):
        return redirect('make_login')

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
        tracker_id = "CTID#{}".format(TrackerMaster.objects.count() + 1)

        if request.GET.get('q'):
            requested_id = request.GET.get('q', '')
            complaints_data = TrackerMaster.objects.filter(complaint_id=requested_id.upper())
        else:
            complaints_data = TrackerMaster.objects.order_by('-reported_date').all()

        if complaints_data.count() > 10:
            paginator = Paginator(complaints_data, 10)
            page = request.GET.get('page', 1)
            try:
                complaints_data = paginator.page(page)
            except EmptyPage:
                complaints_data = paginator.page(paginator.num_pages)
        print(complaints_data)
        return render(request, 'Tracker/index.html',
                      {"page_name": "tracker_home",
                       "login_status": True,
                       "complaint_list": complaints_data,
                       "new_complaint": NewComplaintForm,
                       "tracker_id": tracker_id}
                      )


def make_login(request):
    if request.method == 'POST':

        username = request.POST.get('user_name')
        password = request.POST.get('password')

        if User.objects.get(username=username, password=password):
            return redirect('main_tracker')
        else:
            return redirect('make_login')
    else:
        return render(request, 'Tracker/login.html', {"login_form": UserLoginForm()})
