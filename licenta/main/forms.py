from django import forms 
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField
from django.contrib.auth.models import User
from .models import *
import re

from bootstrap_modal_forms.forms import BSModalModelForm

import datetime

my_default_errors = {
    'required': 'This field is required',
    'invalid': 'Enter a valid value'
}

email_regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$' 

class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].label = 'Email'
        self.fields['password'].label = 'Parola'
    class Meta:
        model = User
        fields = ["username", "password"]

    


class RegisterForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields['username'].label = 'Nume utilizator'
        # self.fields['username'].help_text = "Camp obligatoriu. Maximum 150 caractere. Se accepta doar litere, cifre si caracterele: @/./+/-/_"
        self.fields['username'].label = 'Email'
        self.fields['username'].help_text = "Profesorii sunt rugati sa foloseasca un email institutional"
        # self.fields['email'].label = 'Email'
        # self.fields['email'].help_text = "Profesorii sunt rugati sa foloseasca un email institutional"
        self.fields['password1'].label = 'Parola'
        self.fields['password1'].help_text = "Parola nu poate fi similara cu datele anterioare." + '\n' +  "Parola trebuie sa contina minimim 8 caractere." + '\n' + "Parola nu poate fi in intregime numerica"
        self.fields['password2'].label = 'Repetati parola'
        self.fields['password2'].help_text = 'Introduceti aceeasi parola pentru verificare'
        self.fields['first_name'].label = 'Prenume'
        self.fields['last_name'].label = 'Nume'


    # email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    username = forms.EmailField(required=True)
    class Meta:
        model = User
        # fields = ["username", "email", "last_name", "first_name", "password1", "password2"]
        fields = ["username", "last_name", "first_name", "password1", "password2"]

    def clean(self):
        super(RegisterForm, self).clean()

        email = self.cleaned_data.get('username')

        if re.search(email_regex,email): 
            pass
        else:
            self._errors['username'] = self.error_class([
                'Email invalid'])

        return self.cleaned_data


class CourseForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['topic'].label = 'Tematica'
        self.fields['description'].label = 'Descriere'
        self.fields['date'].label = 'Data'
        self.fields['startTime'].label = 'Ora de inceput'
        self.fields['duration'].label = 'Durata'
        self.fields['lectureHall'].label = 'Sala de curs'
        self.fields['lectureHall'].choices = LectureHall.getAllLectureHalls()
        self.fields['professor'].label = 'Profesor'

   
    date = forms.DateField(required=True, widget=forms.DateInput(attrs={'type': 'date',  'min': datetime.date.today()}))
    startTime = forms.TimeField(required=True, widget=forms.TimeInput(attrs={'type': 'time'}))
    description = forms.CharField(required=False, widget=forms.Textarea(attrs={'class': 'form-control col-md-10 col-lg-10','rows' : 5, 'maxlength': 200}), label="Text")
    professor = forms.ModelChoiceField(required=True, queryset=User.objects.filter(groups__name='Professor'),  to_field_name="email", blank=False)

    class Meta:
        model = Course
        fields = ["topic", "description", "date", "startTime", "duration", "professor", "lectureHall"]

    def clean(self):
        super(CourseForm, self).clean()

        topic = self.cleaned_data.get("topic")
        if len(topic) > 50:
            self._errors['topic'] = self.error_class([
                'Prea multe caractere introduse'])

        return self.cleaned_data




class LectureHallForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].label = 'Nume'
        self.fields['floor'].label = 'Etaj'
        self.fields['maxCapacity'].label = 'Capacitate maxima'
        self.fields['maxCapacity'].help_text = 'Numarul maxim de participanti'

    class Meta:
        model = LectureHall
        fields = ["name", "floor", "maxCapacity"]

    def clean(self):
        super(LectureHallForm, self).clean()

        return self.cleaned_data


class FileCourseResourceForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['file_resource'].label = 'Adauga un fisier'
        self.fields['file_resource'].help_text = 'Adăugati numai fisiere de tip PDF'

    class Meta:
        model = FileCourseResource
        fields = ["file_resource"]

    def clean(self):
        super(FileCourseResourceForm, self).clean()

        return self.cleaned_data
       

class LinkCourseResourceForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['link_resource'].label = 'Adauga un link'
        
    class Meta:
        model = LinkCourseResource
        fields = ["link_resource"]

    def clean(self):
        super(LinkCourseResourceForm, self).clean()

        return self.cleaned_data

class CourseReviewForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['content'].label = 'Scrie un review'
        self.fields['content'].help_text = 'Maxim 600 de caractere'

    class Meta:
        model = CourseReview
        fields = ["content"]

    def clean(self):
        super(CourseReviewForm, self).clean()

        return self.cleaned_data


class AnnouncementForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].label = 'Titlu'
        self.fields['content'].label = 'Anunt'
        self.fields['important'].label = 'Important'

    class Meta:
        model = Announcements
        fields = ["title", "content", "important"]

    def clean(self):
        super(AnnouncementForm, self).clean()

        return self.cleaned_data


class EventForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].label = 'Titlu'
        self.fields['content'].label = 'Detalii eveniment'
        self.fields['date'].label = "Data"
        
    date = forms.DateField(required=True, widget=forms.DateInput(attrs={'type': 'date',  'min': datetime.date.today()}))

    class Meta:
        model = Event
        fields = ["title", "content", "date"]

    def clean(self):
        super(EventForm, self).clean()

        return self.cleaned_data


class UserUpdateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Email'
        # self.fields['email'].label = 'Email'
        self.fields['first_name'].label = "Prenume"
        self.fields['last_name'].label = "Nume"


    # email = forms.EmailField()
    first_name = forms.CharField()
    last_name = forms.CharField()

    class Meta:
        model = User
        # fields = ['username', 'email', 'last_name', 'first_name']
        fields = ['username', 'last_name', 'first_name']

    def clean(self):
        super(UserUpdateForm, self).clean()

        return self.cleaned_data


class ProfileUpdateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['profilePicture'].label = 'Poza profil'
        self.fields['profilePicture'].help_text = 'Pozele cu dimensiuni mai mari de 150x150 for fi redimensionate'
        self.fields['description'].label = 'Descrire'

    profilePicture = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control-file'}))

    class Meta:
        model = Profile
        fields = ['profilePicture', 'description']

    def clean(self):
        super(ProfileUpdateForm, self).clean()

        return self.cleaned_data

