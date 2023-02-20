from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Professor)
admin.site.register(Student)
admin.site.register(Course)
admin.site.register(CourseReview)
admin.site.register(LinkCourseResource)
admin.site.register(FileCourseResource)
admin.site.register(Announcements)
admin.site.register(Event)
admin.site.register(Profile)
