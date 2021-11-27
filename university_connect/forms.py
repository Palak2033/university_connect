from django import forms
from django.forms import Form

from .models import Announcement, Course, Faculty, Semester, Subject


class DateInput(forms.DateInput):
    """Class to take date input
    """

    input_type = "date"


class AddStudentForm(forms.Form):
    """Form to add new students
    """

    email = forms.EmailField(
        label="Email",
        max_length=50,
        widget=forms.EmailInput(attrs={"class": "form-control"}),
    )
    password = forms.CharField(
        label="Password",
        max_length=50,
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
    )
    first_name = forms.CharField(
        label="First Name",
        max_length=50,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    last_name = forms.CharField(
        label="Last Name",
        max_length=50,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    username = forms.CharField(
        label="Username",
        max_length=50,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    address = forms.CharField(
        label="Address",
        max_length=50,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )

    # For Displaying Course
    try:
        Course = Course.objects.all()
        course_list = []
        for course in Course:
            single_course = (course.id, course.course_name)
            course_list.append(single_course)
    except:
        course_list = []

    # For Displaying Semesters
    try:
        semesters = Semester.objects.all()
        semester_list = []
        for semester in semesters:
            single_semester = (
                semester.id,
                str(semester.start_year) + " to " + str(semester.end_year),
            )
            semester_list.append(single_semester)

    except:
        semester_list = []

    gender_list = (("Male", "Male"), ("Female", "Female"))

    course_id = forms.ChoiceField(
        label="Course",
        choices=course_list,
        widget=forms.Select(attrs={"class": "form-control"}),
    )
    gender = forms.ChoiceField(
        label="Gender",
        choices=gender_list,
        widget=forms.Select(attrs={"class": "form-control"}),
    )
    semester_id = forms.ChoiceField(
        label="Semester",
        choices=semester_list,
        widget=forms.Select(attrs={"class": "form-control"}),
    )
    profile_pic = forms.FileField(
        label="Profile Pic",
        required=False,
        widget=forms.FileInput(attrs={"class": "form-control"}),
    )


class EditStudentForm(forms.Form):
    """Form to edit students
    """

    email = forms.EmailField(
        label="Email",
        max_length=50,
        widget=forms.EmailInput(attrs={"class": "form-control"}),
    )
    first_name = forms.CharField(
        label="First Name",
        max_length=50,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    last_name = forms.CharField(
        label="Last Name",
        max_length=50,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    username = forms.CharField(
        label="Username",
        max_length=50,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    address = forms.CharField(
        label="Address",
        max_length=50,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )

    # For Displaying Course
    try:
        Course = Course.objects.all()
        course_list = []
        for course in Course:
            single_course = (course.id, course.course_name)
            course_list.append(single_course)
    except:
        course_list = []

    # For Displaying Semesters
    try:
        semesters = Semester.objects.all()
        semester_list = []
        for semester in semesters:
            single_semester = (
                semester.id,
                str(semester.start_year) + " to " + str(semester.end_year),
            )
            semester_list.append(single_semester)

    except:
        semester_list = []

    gender_list = (("Male", "Male"), ("Female", "Female"))

    course_id = forms.ChoiceField(
        label="Course",
        choices=course_list,
        widget=forms.Select(attrs={"class": "form-control"}),
    )
    gender = forms.ChoiceField(
        label="Gender",
        choices=gender_list,
        widget=forms.Select(attrs={"class": "form-control"}),
    )
    semester_id = forms.ChoiceField(
        label="Semester",
        choices=semester_list,
        widget=forms.Select(attrs={"class": "form-control"}),
    )
    profile_pic = forms.FileField(
        label="Profile Pic",
        required=False,
        widget=forms.FileInput(attrs={"class": "form-control"}),
    )


class AnnouncementForm(forms.ModelForm):
    """Model Form to make a new announcement
    """

    class Meta:
        model = Announcement
        fields = ("subject_id", "message", "link", "upload_url")

    def __init__(self, user, *args, **kwargs):
        super(AnnouncementForm, self).__init__(*args, **kwargs)
        self.fields["subject_id"].queryset = Subject.objects.filter(
            faculty_id=user
        )

    subject_id = forms.ModelChoiceField(
        label="Subject",
        empty_label=None,
        queryset=None,
        to_field_name="subject_name",
        widget=forms.Select(attrs={"class": "form-control"}),
    )
    message = forms.CharField(
        label="Message",
        max_length=400,
        widget=forms.Textarea(attrs={"class": "form-control"}),
    )
    link = forms.URLField(
        label="URL",
        required=False,
        widget=forms.URLInput(attrs={"class": "form-control"}),
    )
    upload_url = forms.FileField(
        label="Upload a File",
        required=False,
        widget=forms.ClearableFileInput(attrs={"class": "form-control"}),
        help_text="File size must not exceed 42 MB",
    )


class EditAnnouncementForm(forms.ModelForm):
    """Model Form to edit an existing announcement
    """

    class Meta:
        model = Announcement
        fields = ("subject_id", "message", "link", "upload_url")

    def __init__(self, user, *args, **kwargs):
        super(EditAnnouncementForm, self).__init__(*args, **kwargs)
        self.fields["subject_id"].queryset = Subject.objects.filter(
            faculty_id=user
        )

    subject_id = forms.ModelChoiceField(
        label="Subject",
        empty_label="--------",
        required=False,
        queryset=None,
        to_field_name="subject_name",
        widget=forms.Select(attrs={"class": "form-control"}),
    )
    message = forms.CharField(
        label="Message",
        required=False,
        max_length=400,
        widget=forms.Textarea(attrs={"class": "form-control"}),
    )
    link = forms.URLField(
        label="URL",
        required=False,
        widget=forms.URLInput(attrs={"class": "form-control"}),
    )
    upload_url = forms.FileField(
        label="Upload a File",
        required=False,
        widget=forms.ClearableFileInput(attrs={"class": "form-control"}),
        help_text="File size must not exceed 42 MB",
    )
