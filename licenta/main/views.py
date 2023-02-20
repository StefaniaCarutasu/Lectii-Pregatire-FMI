from django.shortcuts import render, redirect, get_object_or_404
from django.utils.safestring import mark_safe
from  .forms import *
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from datetime import timedelta, date

# importing group class from django
from django.contrib.auth.models import Group, Permission
from django.contrib.auth.mixins import PermissionRequiredMixin

from django.views.generic.list import ListView
from django.views.generic.edit import DeleteView
from django.views.generic.detail import DetailView
from django.views.generic import FormView
from django.views import generic

from django.http import HttpResponseRedirect

from django.urls import reverse_lazy

from django.contrib.auth.models import User
from bootstrap_modal_forms.generic import BSModalCreateView

from calendar import HTMLCalendar

from .utils import Calendar

from django.shortcuts import render
from django.http import HttpResponse
from django.views import generic
from django.utils.safestring import mark_safe
from django.core.files.storage import default_storage

from .models import *
from .decorators import *

from django.contrib import messages

import calendar
import datetime
import pyrebase
import os

config  = {
  "apiKey": "AIzaSyCppTjErB5IDXrHbIzdMchwZPPDMpHwmVQ",
  "authDomain": "lectiipregatirefmi.firebaseapp.com",
  "projectId": "lectiipregatirefmi",
  "storageBucket": "lectiipregatirefmi.appspot.com",
  "messagingSenderId": "329784597956",
  "appId": "1:329784597956:web:3534f7b2f89b8fe639d891",
  "measurementId": "G-THC7PSZW5X",
  "databaseURL": ""
}

firebase = pyrebase.initialize_app(config)
storage = firebase.storage()


# Create your views here.
def home(request):
    return render(request, 'main/home.html')

def error_404(request, exception):
    response = render_to_response('static_pages/404.html',context_instance=RequestContext(request))
    response.status_code = 404
    return response

def error_403(request, exception):
    response = render_to_response('static_pages/403.html',context_instance=RequestContext(request))
    response.status_code = 403
    return response

def page_not_found(request):
    return render(request, 'static_pages/404.html')

def page_forbidden(request):
    return render(request, 'static_pages/403.html')    

# register form
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.email = user.username
            user.save() 

            if user.email.endswith('@unibuc.ro') or user.email.endswith('@fmi.unibuc.ro'):
                group = Group.objects.get(name="professor")
                group.user_set.add(user)
            else:
                group = Group.objects.get(name="student")
                group.user_set.add(user)                      

            login(request, user)

            return redirect('/list-courses')
    else:
        form = RegisterForm()

    return render(request, 'registration/register.html', {"form": form})


# login form
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username,password=password)
        if user:
            if user.is_active:
                login(request, user)
                return redirect('/list-courses')
        else:
            return redirect('/login')
        
                
    else:
        form = LoginForm()
    return render(request,'registration/login.html',{'form':form})

###################################################################################################

# PROFILE
def user_profile(request):
    user = request.user
    context = {}
    context["user"] = user

    
    if user.groups.filter(name = 'professor').exists():
        context['type'] = 'professor'
        courses = Course.objects.select_related("lectureHall").filter(professor = user)
        context['courses'] = courses
    else: 
        context['type'] = 'student'

    profile = Profile.objects.filter(user = user).first()
    context['profile'] = profile

    today_min = datetime.datetime.combine(datetime.date.today(), datetime.time.min)
    today_max = datetime.datetime.combine(datetime.date.today(), datetime.time.max)
    current_events = Event.objects.filter(date__range=(today_min, today_max))
    
    context['events'] = current_events

    return render(request, "main/profile/profile.html", context)

def update_profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            request.user.email = request.user.username
            p_form.save()
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'main/profile/update_profile.html', context)



###################################################################################################
# LECTURE HALLS CRUD

# new lecture hall form
@login_required(login_url='/login')
def new_lecture_hall(request):
    if request.method == 'POST':
        form = LectureHallForm(request.POST)
        
        if form.is_valid():
            lecture_hall = form.save()
            messages.success(request, 'Amfiteatru adaugat cu succes')

            return redirect('/list-lecture-halls')
        
    else:
        form = LectureHallForm()

    return render(request, 'main/lecture_hall/new_lecture_hall.html', {"form": form})

class LectureHallsList(ListView):
    model = LectureHall
    template_name = 'main/lecture_hall/list-lecture-halls.html'

def update_lecture_hall(request, id):
    context = {}
    # fetch the object related to passed id
    obj = get_object_or_404(LectureHall, id = id)
 
    # pass the object as instance in form
    form = LectureHallForm(request.POST or None, instance = obj)
 
    # save the data from the form and
    # redirect to detail_view
    if form.is_valid():
        form.save()
        messages.success(request, 'Amfiteatru editat cu succes')
        return HttpResponseRedirect("/list-lecture-halls")
 
    # add form dictionary to context
    context["form"] = form
 
    return render(request, "main/lecture_hall/update_lecture_hall.html", context)

class DeleteLectureHall(DeleteView):
    # specify the model you want to use
    model = LectureHall
     
    template_name = "main/lecture_hall/lecture_hall_delete_confirm.html" 
    # can specify success url
    # url to redirect after successfully
    # deleting object
    success_url ="/list-lecture-halls"


###################################################################################################

# COURSES CRUD
# list courses
# @login_required(login_url='/login')
class CoursesList(ListView):
    model = Course
    template_name = 'main/course/list-courses.html'

    def get_context_data(self, *args, **kwargs):
        context = super(CoursesList,
             self).get_context_data(*args, **kwargs)
        if self.request.user.groups.filter(name = "student").exists():
            context['type'] = 'student'
        else:
            context['type'] = 'professor'
        
        return context

# new course view
@login_required(login_url='/login')
@check_permissions
def new_course(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        
        if form.is_valid():
            course = form.save(commit=False)
            if not form.data['professor']:
                course.professor = request.user
            course.save()
            event = Event(title = course.topic, content = course.description, date = course.date, author = request.user)
            # event.save()
            messages.success(request, 'Lectie adaugata cu succes')

            return redirect('/list-courses')
        
    else:
        form = CourseForm()

    return render(request, 'main/course/new_course.html', {"form": form})

# display course view
class ViewCourse(DetailView):
    template_name = "main/course/display-course.html"
    model = Course

    context_object_name = "course" 

    # override context data
    def get_context_data(self, *args, **kwargs):
        context = super(ViewCourse,
             self).get_context_data(*args, **kwargs)
        # add extra fields
        context["lectureHall"] = get_object_or_404(LectureHall, id=context["course"].lectureHall.id)      
        context["professor"] = get_object_or_404(User, id=context["course"].professor.id)
        if self.request.user.groups.filter(name = "student").exists():
            context["reviews"] = CourseReview.objects.filter(course=context["course"].id, user = self.request.user.id)
        else:
            context["reviews"] = CourseReview.objects.filter(course=context["course"].id)
        context["fileResources"] = FileCourseResource.objects.filter(course=context["course"].id)
        context["linkResources"] = LinkCourseResource.objects.filter(course=context["course"].id)
        

        return context
        
@login_required(login_url='/login')
def new_review(request, id):
    if request.method == 'POST':
        form = CourseReviewForm(request.POST)
        
        if form.is_valid():
            review = form.save(commit=False)
            review.course = get_object_or_404(Course, id = id)
            review.user = request.user
            review.save()
            messages.success(request, 'Review adaugat cu succes')

            return redirect('/display-course/' + id)
        
    else:
        form = CourseReviewForm()

    return render(request, 'main/course/new_review.html', {"form": form, "course_id": id})

@check_permissions
def new_link_resource(request, id):
    if request.method == 'POST':
        form = LinkCourseResourceForm(request.POST)
        
        if form.is_valid():
            resource = form.save(commit=False)
            resource.course = get_object_or_404(Course, id = id)
            resource.save()
            messages.success(request, 'Resursa adaugata cu succes')

            return redirect('/display-course/' + id)
        
    else:
        form = LinkCourseResourceForm()

    return render(request, 'main/course/new_link_resource.html', {"form": form, "course_id": id})

@check_permissions
def new_file_resource(request, id):
    if request.method == 'POST':
        form = FileCourseResourceForm(request.POST, request.FILES)
        file = request.FILES['file_resource']
        
        if form.is_valid():
            resource = form.save(commit=False)
            resource.course = get_object_or_404(Course, id = id)
            resource.file_name = file.name
            # resource.folder_name = id
           
            #file_save = default_storage.save("resources/" + id + "/" + file.name, file)
            #storage.child("resources/" + id + '/' + file.name).put("media/resources/" + id + "/" + file.name)
            #delete = default_storage.delete(file.name)
            resource.save()
            messages.success(request, 'Resursa adaugata cu succes')
            return redirect('/display-course/' + id)
        
    else:
        form = FileCourseResourceForm()

    return render(request, 'main/course/new_file_resource.html', {"form": form, "course_id": id})

@check_permissions
def delete_file_resource(request, id):
    # dictionary for initial data with
    # field names as keys
    context ={}
 
    # fetch the object related to passed id
    obj = get_object_or_404(FileCourseResource, id = id)
    course_id = obj.course.id
    context["object"] = obj

    if request.method =="POST":
        # delete object
        obj.delete()
        delete = default_storage.delete("resources/" + obj.file_name)
        
        # after deleting redirect to
        # home page
        return HttpResponseRedirect("/display-course/" + str(course_id))
 
    return render(request, "main/course/file_resource_delete_confirm.html", context)

@login_required(login_url='/login')
def display_resource(request, id):
    # dictionary for initial data with
    # field names as keys
    context ={}
    file = FileCourseResource.objects.get(id = id)
    # add the dictionary during initialization
    context["file"] = file
         
    return render(request, "main/course/display_resource.html", context)

@check_permissions
def delete_link_resource(request, id):
    # dictionary for initial data with
    # field names as keys
    context ={}
 
    # fetch the object related to passed id
    obj = get_object_or_404(LinkCourseResource, id = id)
    course_id = obj.course.id
    context["object"] = obj

    if request.method =="POST":
        # delete object
        obj.delete()

        return HttpResponseRedirect("/display-course/" + str(course_id))
 
    return render(request, "main/course/link_resource_delete_confirm.html", context)



def delete_review(request, id):
    # dictionary for initial data with
    # field names as keys
    context ={}
 
    # fetch the object related to passed id
    obj = get_object_or_404(CourseReview, id = id)
    course_id = obj.course.id
    context["object"] = obj

    if request.method =="POST":
        # delete object
        obj.delete()

        return HttpResponseRedirect("/display-course/" + str(course_id))
 
    return render(request, "main/course/review_delete_confirm.html", context)

@check_permissions
class DeleteLinkResource(DeleteView):
    # specify the model you want to use
    model = LinkCourseResource
     
    template_name = "main/course/link_resource_delete_confirm.html" 

    success_url = '/list-courses'

@check_permissions
class DeleteFileResource(DeleteView):
    # specify the model you want to use
    model = FileCourseResource
     
    template_name = "main/course/file_resource_delete_confirm.html" 

    success_url = '/list-courses'

# update course view
def update_review(request, id):
    if request.method == 'POST':
        
        # fetch the object related to passed id
        obj = get_object_or_404(CourseReview, id = id)
        course_id = obj.course
    
        # pass the object as instance in form
        form = CourseReviewForm(request.POST or None, instance = obj)
    
        # save the data from the form and
        # redirect to detail_view
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/display-course/" + course_id)
    else: 
        context = {}
        # add form dictionary to context
        obj = get_object_or_404(CourseReview, id = id)
    
        # pass the object as instance in form
        form = CourseReviewForm(request.POST or None, instance = obj)
        context["form"] = form
 
    return render(request, "main/course/update_review.html", context)


@check_permissions
def new_link_resource(request, id):
    if request.method == 'POST':
        form = LinkCourseResourceForm(request.POST)
        
        if form.is_valid():
            resource = form.save(commit=False)
            resource.course = get_object_or_404(Course, id = id)
            # resource.user = request.user
            resource.save()

            return redirect('/display-course/' + id)
        
    else:
        form = LinkCourseResourceForm()

    return render(request, 'main/course/new_link_resource.html', {"form": form, "course_id": id})


# update course view
@check_permissions
def update_course(request, id):
    context = {}
    obj = get_object_or_404(Course, id = id)
 
    form = CourseForm(request.POST or None, instance = obj)
 
    if form.is_valid():
        form.save()

        return HttpResponseRedirect("/display-course/" + id)

    context["form"] = form
 
    return render(request, "main/course/update_course.html", context)

# @check_permissions
class DeleteCourse(DeleteView):
    # specify the model you want to use
    model = Course
     
    template_name = "main/course/course_delete_confirm.html" 
    # can specify success url
    # url to redirect after successfully
    # deleting object
    success_url ="/list-courses"



# CREATE RESOURCES
class LinkResourceView(BSModalCreateView):
    def __init__(self, *args, **kwargs):
        from django.forms.widgets import HiddenInput
        course = kwargs.pop('course',None)
        super(LinkCourseResourceForm, self).__init__(*args, **kwargs)
        if course:
            self.fields['course'].widget = HiddenInput()
            

    template_name = 'course/new_link_resource.html'
    form_class = LinkCourseResource
    
    success_url = reverse_lazy('display-course/form.course.id')


###################################################################################################

# CRUD FOR ANNOUNCEMENTS

# list announcements
class AnnouncementsList(ListView):
    model = Announcements
    template_name = 'main/announcement/list-announcements.html'

# new announcement
def new_announcement(request):
    if request.method == 'POST':
        form = AnnouncementForm(request.POST)
        
        if form.is_valid():
            announcement = form.save(commit=False)
            announcement.author = request.user
            announcement.date = datetime.datetime.now()  
            announcement.save()

            messages.success(request, 'Anunt adaugat cu succes')

            return redirect('/list-announcements')
        
    else:
        form = AnnouncementForm()

    return render(request, 'main/announcement/new_announcement.html', {"form": form})

# update announcement view
def update_announcement(request, id):
    context = {}
    # fetch the object related to passed id
    obj = get_object_or_404(Announcements, id = id)
 
    # pass the object as instance in form
    form = AnnouncementForm(request.POST or None, instance = obj)
 
    # save the data from the form and
    # redirect to detail_view
    if form.is_valid():
        form.save()
        return HttpResponseRedirect("/list-announcements")
 
    # add form dictionary to context
    context["form"] = form
 
    return render(request, "main/announcement/update_announcement.html", context)

class DeleteAnnouncement(DeleteView):
    # specify the model you want to use
    model = Announcements
     
    template_name = "main/announcement/announcement_delete_confirm.html" 
    # can specify success url
    # url to redirect after successfully
    # deleting object
    success_url ="/list-announcements"

###################################################################################################
# EVENIMENTE
class EventsList(ListView):
    model = Event
    template_name = 'main/event/list-events.html'

# new event view
def new_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        
        if form.is_valid():
            event = form.save(commit=False)
            event.created_at = date.today()
            event.author = request.user
            event.save()
            messages.success(request, 'Eveniment adaugat cu succes')

            return redirect('/list-events')
        
    else:
        form = EventForm()

    return render(request, 'main/event/new_event.html', {"form": form})

# update event view
def update_event(request, id):
    context = {}
    # fetch the object related to passed id
    obj = get_object_or_404(Event, id = id)
 
    # pass the object as instance in form
    form = EventForm(request.POST or None, instance = obj)
 
    # save the data from the form and
    # redirect to detail_view
    if form.is_valid():
        form.save()
        return HttpResponseRedirect("/list-events")
 
    # add form dictionary to context
    context["form"] = form
 
    return render(request, "main/event/update_event.html", context)

class DeleteEvent(DeleteView):
    # specify the model you want to use
    model = Event
     
    template_name = "main/event/event_delete_confirm.html" 
    # can specify success url
    # url to redirect after successfully
    # deleting object
    success_url ="/list-events"

# display eventViewEvent view
def display_event(request, id):
    # dictionary for initial data with
    # field names as keys
    context ={}
    object = Event.objects.get(id = id)
    # add the dictionary during initialization
    context["object"] = object
         
    return render(request, "main/event/display-event.html", context)

class ViewEvent(DetailView):
    template_name = "main/event/display-event.html"
    model = Event

###################################################################################################

class CalendarView(generic.ListView):
    model = Event
    template_name = 'calendar/calendar.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        d = get_date(self.request.GET.get('month', None))
        cal = Calendar(d.year, d.month)
        html_cal = cal.formatmonth(withyear=True)
        context['calendar'] = mark_safe(html_cal)
        context['prev_month'] = prev_month(d)
        context['next_month'] = next_month(d)
        return context

def get_date(req_month):
    if req_month:
        year, month = (int(x) for x in req_month.split('-'))
        return date(year, month, day=1)
    return datetime.datetime.today()

def prev_month(d):
    first = d.replace(day=1)
    prev_month = first - timedelta(days=1)
    month = 'month=' + str(prev_month.year) + '-' + str(prev_month.month)
    return month

def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = 'month=' + str(next_month.year) + '-' + str(next_month.month)
    return month
