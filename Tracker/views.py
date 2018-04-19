from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage
from .models import TrackerMaster, TrackerStatus, TrackerUsers, Department, ResponseMessage
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .forms import NewComplaintForm, UserLoginForm, NewNotification


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
                       "responses": NewNotification,
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
                      {"page_name": "tracker_out_bound",
                       "login_status": True,
                       "complaint_list": complaints_data,
                       "new_complaint": NewComplaintForm,
                       "tracker_id": tracker_id}
                      )


def notification(request):
    # redirect login page if session not enabled
    dept_id = request.session.get('user_department')
    if not dept_id:
        return redirect('make_login')

    if request.method == 'GET':
        tracker_id = "CTID#{}".format(TrackerMaster.objects.count() + 1)
        dept = Department.objects.get(id=int(dept_id))
        message_data = ResponseMessage.objects.filter(to_department=dept).order_by('-created_date')

        if message_data.count() > 10:
            paginator = Paginator(message_data, 10)
            page = request.GET.get('page', 1)
            try:
                message_data = paginator.page(page)
            except EmptyPage:
                message_data = paginator.page(paginator.num_pages)
        return render(request, 'Tracker/notifications.html',
                      {"page_name": "notifications",
                       "login_status": True,
                       "message_list": message_data,
                       "new_complaint": NewComplaintForm,
                       "tracker_id": tracker_id}
                      )


def send_message(request):
    if request.method == 'POST':
        input_data = NewNotification(request.POST)
        if input_data.is_valid():
            input_data_stream = input_data.save(commit=False)
            tracker_obj = TrackerMaster.objects.get(id=int(request.POST.get("response_to_complaint")))
            input_data_stream.from_department = tracker_obj.to_department
            input_data_stream.to_department = tracker_obj.from_department
            input_data_stream.save()
        else:
            print("error")
        return redirect('main_tracker')


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


def ajax_mark_as_resolved(request):
    complaint_id = int(request.POST.get('complaint_id', ''))
    status_obj = TrackerStatus.objects.get(id=2)
    TrackerMaster.objects.filter(id=complaint_id).update(complaint_status=status_obj)
    return HttpResponse("success")


def ajax_delete_entry(request):
    # complaint_id = int(request.POST.get('complaint_id', ''))
    # TrackerMaster.objects.filter(id=complaint_id).delete()
    return HttpResponse(5)
