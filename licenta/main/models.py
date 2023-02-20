from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django.utils import timezone
from .validators import validate_file_extension


# Create your models here.
# Model for the lecture hall
class LectureHall(models.Model):
    name = models.CharField(max_length = 30)
    floor = models.IntegerField()
    maxCapacity = models.IntegerField()

    @classmethod
    def getAllLectureHalls(cls):
        objectlist = LectureHall.objects.all()

        hallsTuple = [(object.id, object.name) for object in objectlist]

        return hallsTuple  

# Model for the course
class Course(models.Model):
    professor = models.ForeignKey(User, on_delete=models.CASCADE)
    topic = models.CharField(max_length=50)
    description = models.TextField(blank=True, max_length=200)
    lectureHall = models.ForeignKey(LectureHall, null=True, on_delete=models.SET_NULL)
    date = models.DateTimeField()
    startTime = models.TimeField()
    duration = models.IntegerField()



# Model for professor profile
class Professor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profilePicture = models.ImageField(default='default.jpg', upload_to='profile_pics', blank=True)
    description = models.CharField(max_length=200, blank=True)
    specialization = models.CharField(max_length=50, blank=True)
    title = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return f'{self.user.username} Profile'
    


# Model for student profile
class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profilePicture = models.ImageField(default='default.jpg', upload_to='profile_pics', blank=True)
    grade = models.IntegerField(blank=True, null=True)
    school= models.CharField(max_length=50, blank=True)
    city = models.CharField(max_length=50, blank=True)
    county = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return f'{self.user.username} Profile'

# Model for profile
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profilePicture = models.ImageField(default='default.jpg', upload_to='profile_pics')
    description = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)

        img = Image.open(self.profilePicture.path)

        if img.height > 150:
            resized = img.resize((150, img.width), Image.ANTIALIAS)
            resized.save(self.profilePicture.path)
        elif img.width > 150:
            resized = img.resize((img.height, 150), Image.ANTIALIAS)
            resized.save(self.profilePicture.path)


# Model for the review
class CourseReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)
    content = models.TextField(max_length=600)


# Model for course resources
class LinkCourseResource(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    link_resource = models.CharField(max_length=200)
   

class FileCourseResource(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    # file_resource = models.FileField(upload_to="resources", validators=[validate_file_extension])
    file_resource = models.FileField(upload_to="resources")
    file_name = models.CharField(max_length=100)

class Announcements(models.Model):
    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=30)
    content = models.TextField()
    date = models.DateTimeField()
    important = models.BooleanField()

class Event(models.Model):
    title = models.CharField(max_length=50)
    content = models.TextField()
    date = models.DateTimeField()
    created_at = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

