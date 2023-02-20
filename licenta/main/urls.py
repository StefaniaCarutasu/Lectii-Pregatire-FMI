from django.urls import path, re_path
from django.conf.urls import handler404, handler403
from django.conf import settings
from django.conf.urls.static import static
from . import views
from django.contrib.auth.views import LoginView
from . import forms
from django.contrib.auth import views as auth_views
from .views import CoursesList, ViewCourse, update_course, AnnouncementsList, error_404, update_announcement, EventsList, LectureHallsList, ViewEvent


from django.conf import settings
from django.conf.urls.static import static

handler404 = 'main.views.error_404'
handler403 = 'main.views.error_403'

urlpatterns = [
    path("", views.home, name='home'),
    path("home", views.home, name='home'),
    path("register", views.register, name='register'),
    # path('login/', LoginView.as_view( template_name="registration/login.html",  authentication_form=forms.LoginForm ), name='login')
    path('login/', views.login_view, name='login'),

     path('password-reset/',
         auth_views.PasswordResetView.as_view(
             template_name='password_reset/password_reset.html',
              html_email_template_name='password_reset\password_reset_email.html'
         ),
         name='password_reset'),
    path('password_reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='password_reset/password_reset_done.html'
         ),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='password_reset/password_reset_confirm.html'
         ),
         name='password_reset_confirm'),
    path('reset/done/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='password_reset/password_reset_complete.html'
         ),
         name='password_reset_complete'),
    
     # lecture halls
    path("list-lecture-halls", LectureHallsList.as_view(), name='list-lecture-halls'),
    path("new-lecture-hall", views.new_lecture_hall, name='new-lecture-hall'),
    path('<id>/update_lecture_hall', views.update_lecture_hall, name = "update_lecture_hall" ),
    path('<pk>/delete_lecture_hall/', views.DeleteLectureHall.as_view(),  name = "delete-lecture-hall"),

    # courses
    path("new-course", views.new_course, name='new-course'),
    path("list-courses", CoursesList.as_view(), name='list-courses'),
    path("display-course/<pk>/", ViewCourse.as_view(), name = 'display-course'),
    path('<id>/update', update_course, name = "update-course" ),
    path('<pk>/delete_course/', views.DeleteCourse.as_view(), name = "delete-course" ),

    # reviews
    path('new_review/<id>', views.new_review, name = "new_review" ),
    # path('delete_review/<pk>', views.DeleteReview.as_view(),  name = "delete-review"),
    path('delete_review/<id>', views.delete_review,  name = "delete-review"),
    path('update_review/<id>/', views.update_review, name = "update-review" ),

    # link resources
    path('new_link_resource/<id>', views.new_link_resource, name = "new_link_resource" ),
    # path('delete_link_resource/<pk>', views.DeleteLinkResource.as_view(),  name = "delete-link-resource"),
    path('delete_link_resource/<id>', views.delete_link_resource,  name = "delete-link-resource"),

    # file resources
    path('new_file_resource/<id>', views.new_file_resource, name = "new_file_resource" ),
    path('delete_file_resource/<int:id>', views.delete_file_resource,  name = "delete-file-resource"),
    path("display-resource/<id>/", views.display_resource, name = 'display_resource'),

    # announcements
    path("list-announcements", AnnouncementsList.as_view(), name='list-announcements'),
    path("new-announcement", views.new_announcement, name='new-announcement'),
    path('<id>/update_announcement', update_announcement, name = "update_announcement" ),
    path('<pk>/delete_announcement/', views.DeleteAnnouncement.as_view(),  name = "delete-announcement"),

    # events
    path("list-events", EventsList.as_view(), name='list-events'),
    path("new-event", views.new_event, name='new-event'),
    path('<id>/update_event', views.update_event, name = "update_event" ),
    # path('<id>/delete_event', views.delete_event, name = "delete-event" ),
    path('<pk>/delete_event/', views.DeleteEvent.as_view(),  name = "delete-event"),
    path("calendar/display-event/<id>/", views.display_event, name = 'display-event'),

    # calendar
    # path("calendar", views.CalendarView.as_view(), name="calendar"),
    re_path(r'^calendar/$', views.CalendarView.as_view(), name='calendar'),

    # profile
    path("profile", views.user_profile, name="profile"),
    path("update_profile", views.update_profile, name="update_profile"),

    path("404", views.page_not_found),
    path("403", views.page_forbidden),
] 


