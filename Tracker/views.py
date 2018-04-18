from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage
from .models import TrackerMaster, TrackerStatus, TrackerUsers, Department
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .forms import NewComplaintForm, UserLoginForm
# Create your views here.


class Constants:
    processing = 'pending'
    resolved = 'resolved'


def main_tracker(request):
    # redirect login page if session not enabled
    dept_id = request.session.get('user_department')
    if not dept_id:
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
            dept = Department.objects.get(id=int(dept_id))
            complaints_data = TrackerMaster.objects.filter(to_department=dept).order_by('-reported_date')

        if complaints_data.count() > 10:
            paginator = Paginator(complaints_data, 10)
            page = request.GET.get('page', 1)
            try:
                complaints_data = paginator.page(page)
            except EmptyPage:
                complaints_data = paginator.page(paginator.num_pages)
        return render(request, 'Tracker/index.html',
                      {"page_name": "tracker_home",
                       "login_status": True,
                       "complaint_list": complaints_data,
                       "new_complaint": NewComplaintForm,
                       "tracker_id": tracker_id}
                      )


def out_bound_complaints(request):
    # redirect login page if session not enabled
    dept_id = request.session.get('user_department')
    if not dept_id:
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
            dept = Department.objects.get(id=int(dept_id))
            complaints_data = TrackerMaster.objects.filter(from_department=dept).order_by('-reported_date')

        if complaints_data.count() > 10:
            paginator = Paginator(complaints_data, 10)
            page = request.GET.get('page', 1)
            try:
                complaints_data = paginator.page(page)
            except EmptyPage:
                complaints_data = paginator.page(paginator.num_pages)
        return render(request, 'Tracker/outbound.html',
                      {"page_name": "tracker_home",
                       "login_status": True,
                       "complaint_list": complaints_data,
                       "new_complaint": NewComplaintForm,
                       "tracker_id": tracker_id}
                      )


def make_login(request):
    if request.method == 'POST':
        username = request.POST.get('user_name', '')
        password = request.POST.get('user_password', '')

        if authenticate(username=username, password=password):
            user_obj = User.objects.get(username=username).pk
            tracker_user_obj = TrackerUsers.objects.get(user=user_obj)
            dept_obj = tracker_user_obj.department
            request.session["user_department"] = dept_obj.id
            return redirect('main_tracker')
        else:
            return redirect('make_login')
    else:
        if request.session.get('user_department'):
            return redirect('main_tracker')
        else:
            return render(request, 'Tracker/login.html', {"login_form": UserLoginForm()})


def logout_user(request):
    try:
        del request.session["user_department"]
    except KeyError:
        pass
    return redirect('make_login')


# ajax requests
def ajax_mark_as_resolved(request):
    complaint_id = request.POST.get('complaint_id', '')
    print(complaint_id)
    return 
# end
