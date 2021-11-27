from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class BaseUser(AbstractUser):
    """Base User Class: This is the parent class for all different kinds of users and is
    connected as the Django AUTH_USER_MODEL

    Attributes
    ----------
    user_type_data : Tuple
        Represents a tuple of tuples with first values being numeric
        and second values being user type in string format
    user_type : int
        User type 1 for Admin, 2 for Faculty, 3 for Student
    """

    user_type_data = ((1, "Admin"), (2, "Faculty"), (3, "Student"))
    user_type = models.CharField(
        default=1, choices=user_type_data, max_length=10
    )


class Admin(models.Model):
    """Admin Class

    Attributes
    ----------
    id : int
        Primary key
    admin : int
        Primary key of the admin in the BaseUser table
    created_at : datetime.datetime
        Datetime at which the object was created at 
    updated_at : datetime.datetime
        Datetime at which the object was last updated at 
    objects : django.models.Manager
        Static variable which stores all the objects 
        being instantiated with this class
    """

    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(BaseUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


class Faculty(models.Model):
    """Admin Class

    Attributes
    ----------
    id : int
        Primary key
    admin : int
        Primary key of the admin in the BaseUser table
    address : str
        Address of the faculty
    created_at : datetime.datetime
        Datetime at which the object was created at 
    updated_at : datetime.datetime
        Datetime at which the object was last updated at 
    objects : django.models.Manager
        Static variable which stores all the objects 
        being instantiated with this class
    """

    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(BaseUser, on_delete=models.CASCADE)
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

    def __str__(self):
        return self.admin.first_name + " " + self.admin.last_name


class Course(models.Model):
    """Class to represent a Course

    Attributes
    ----------
    id : int
        Primary key
    course_name : str
        String name of the course
    created_at : datetime.datetime
        Datetime at which the object was created at 
    updated_at : datetime.datetime
        Datetime at which the object was last updated at 
    objects : django.models.Manager
        Static variable which stores all the objects 
        being instantiated with this class
    """

    id = models.AutoField(primary_key=True)
    course_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

    def __str__(self):
        return self.course_name


class Subject(models.Model):
    """Class to represent a Subject

    Attributes
    ----------
    id : int
        Primary key
    subject_name : str
        String name of the subject
    course_id : int
        Foreign key of the corresponding course the subject belongs to
    faculty_id : int
        Foreign key of the faculty teaching the subject
    created_at : datetime.datetime
        Datetime at which the object was created at 
    updated_at : datetime.datetime
        Datetime at which the object was last updated at 
    objects : django.models.Manager
        Static variable which stores all the objects 
        being instantiated with this class
    """

    id = models.AutoField(primary_key=True)
    subject_name = models.CharField(max_length=255)
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE, default=1)
    faculty_id = models.ForeignKey(BaseUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

    def __str__(self):
        return self.subject_name


class Semester(models.Model):
    """Class to represent a Semester

    Attributes
    ----------
    id : int
        Primary key
    start_year : datetime.date
        Start date of semester
    end_year : datetime.date
        End date of semester
    objects : django.models.Manager
        Static variable which stores all the objects 
        being instantiated with this class
    """

    id = models.AutoField(primary_key=True)
    start_year = models.DateField()
    end_year = models.DateField()
    objects = models.Manager()

    def __str__(self):
        return str(self.start_year) + " to " + str(self.end_year)


class Student(models.Model):
    """Student Class

    Attributes
    ----------
    id : int
        Primary key
    admin : int
        Primary key of the admin in the BaseUser table
    gender : str
        Gender of the student
    profile_pic : URL
        URL of the profile picture uploaded
    address : str
        Address of the student
    course_id : int
        Foreign key of the corresponding course the student is enrolled in
    semester_id : int
        Foreign key of the corresponding semester the student is enrolled in
    created_at : datetime.datetime
        Datetime at which the object was created at 
    updated_at : datetime.datetime
        Datetime at which the object was last updated at 
    objects : django.models.Manager
        Static variable which stores all the objects 
        being instantiated with this class
    """

    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(BaseUser, on_delete=models.CASCADE)
    gender = models.CharField(max_length=50)
    profile_pic = models.FileField()
    address = models.TextField()
    course_id = models.ForeignKey(
        Course, on_delete=models.DO_NOTHING, default=1
    )
    semester_id = models.ForeignKey(Semester, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

    def __str__(self):
        return self.admin.first_name + " " + self.admin.last_name


class Attendance(models.Model):
    """Class creates a table to store different attendance logs.

    Attributes
    ----------
    id : int
        Primary key
    subject_id : int
        Foreign key of the subject the attendance is being taken for
    attendance_date : datetime.date
        Date for which the attendance is being taken for
    semester_id : int
        Foreign key of the semester in which the attendance is being taken
    created_at : datetime.datetime
        Datetime at which the object was created at 
    updated_at : datetime.datetime
        Datetime at which the object was last updated at 
    objects : django.models.Manager
        Static variable which stores all the objects 
        being instantiated with this class
    """

    id = models.AutoField(primary_key=True)
    subject_id = models.ForeignKey(Subject, on_delete=models.DO_NOTHING)
    attendance_date = models.DateField()
    semester_id = models.ForeignKey(Semester, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


class AttendanceReport(models.Model):
    """Class creates a table to store different attendance logs.

    Attributes
    ----------
    id : int
        Primary key
    subject_id : int
        Foreign key of the subject the attendance is being taken for
    attendance_id : int
        Foreign key corresponding to the Attendance table of the
        subject the student is studying
    status : int
        Attendance status of the student. 0 for absent, 1 for present.
    created_at : datetime.datetime
        Datetime at which the object was created at 
    updated_at : datetime.datetime
        Datetime at which the object was last updated at 
    objects : django.models.Manager
        Static variable which stores all the objects 
        being instantiated with this class
    """

    id = models.AutoField(primary_key=True)
    student_id = models.ForeignKey(Student, on_delete=models.DO_NOTHING)
    attendance_id = models.ForeignKey(Attendance, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


class Feedback(models.Model):
    """Class creates a table to store feedbacks from faculties
    and students for the admins.

    Attributes
    ----------
    id : int
        Primary key
    user : int
        Foreign key of the corresponding user in the BaseUser table.
    feedback : str
        Feedback message
    feedback_reply : int
        Feedback reply
    created_at : datetime.datetime
        Datetime at which the object was created at 
    updated_at : datetime.datetime
        Datetime at which the object was last updated at 
    objects : django.models.Manager
        Static variable which stores all the objects 
        being instantiated with this class
    """

    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(BaseUser, on_delete=models.CASCADE)
    feedback = models.TextField()
    feedback_reply = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


class Announcement(models.Model):
    """Class creates a table to store announcements from faculties
    to the students. Admins will also be able to view/delete them.

    Attributes
    ----------
    id : int
        Primary key
    faculty_id : int
        Foreign key corresponding to the faculty sending the announcement
    subject_id : int
        Foreign key corresponding to the subject of the announcement
    message : str
        Message for the announcement
    link : URL
        Extra URL that can be attached to the text of the announcement
    upload_url : URL
        URL of the file uploaded with the announcement
    upload_name : str
        Name of the file uploaded with the announcement
    read_status : boolean
        Read status of the announcement. True for read, False for unread.
    created_at : datetime.datetime
        Datetime at which the object was created at 
    updated_at : datetime.datetime
        Datetime at which the object was last updated at 
    objects : django.models.Manager
        Static variable which stores all the objects 
        being instantiated with this class
    """

    id = models.AutoField(primary_key=True)
    faculty_id = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    subject_id = models.ForeignKey(Subject, on_delete=models.CASCADE)
    message = models.TextField(blank=True)
    link = models.URLField(blank=True)
    upload_url = models.FileField(
        upload_to=f"assignments/{faculty_id}", blank=True, null=False
    )
    upload_name = models.TextField(blank=True)
    read_status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


class LeaveReport(models.Model):
    """Class creates a table to store leave requests from faculties
    and students for the admins.

    Attributes
    ----------
    id : int
        Primary key
    user : int
        Foreign key corresponding to the user in the BaseUser table
    start_date : datetime.date
        Start date of the leave
    end_date : datetime.date
        End date of the leave
    message : str
        Reason for the leave
    status : int
        Read status of the announcement. 1 for read, 0 for unread.
    created_at : datetime.datetime
        Datetime at which the object was created at 
    updated_at : datetime.datetime
        Datetime at which the object was last updated at 
    objects : django.models.Manager
        Static variable which stores all the objects 
        being instantiated with this class
    """

    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(BaseUser, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    message = models.TextField()
    status = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


class StudentResult(models.Model):
    """Class creates a table to store student results marked by faculties.

    Attributes
    ----------
    id : int
        Primary key
    student_id : int
        Foreign key corresponding to the student in the Student table
    subject_id : int
        Foreign key corresponding to the subject in the Subject table
    exam_marks : float
        Marks for exam
    assignment_marks : float
        Marks for assignment
    created_at : datetime.datetime
        Datetime at which the object was created at 
    updated_at : datetime.datetime
        Datetime at which the object was last updated at 
    objects : django.models.Manager
        Static variable which stores all the objects 
        being instantiated with this class
    """

    id = models.AutoField(primary_key=True)
    student_id = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject_id = models.ForeignKey(Subject, on_delete=models.CASCADE)
    exam_marks = models.FloatField(default=0)
    assignment_marks = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


@receiver(post_save, sender=BaseUser)
def create_user_profile(sender, instance, created, **kwargs):
    """Creates a user profile

    Parameters
    ----------
    sender : BaseUser
        User creating the new profile
    instance : BaseUser
        Data to be stored in the new user
    created : boolean
        If true, instantiate new object of the respective user
    """
    if created:
        if instance.user_type == 1:
            Admin.objects.create(admin=instance)
        if instance.user_type == 2:
            Faculty.objects.create(admin=instance)
        if instance.user_type == 3:
            Student.objects.create(
                admin=instance,
                course_id=Course.objects.get(id=1),
                semester_id=Semester.objects.get(id=1),
                address="",
                profile_pic="",
                gender="",
            )


@receiver(post_save, sender=BaseUser)
def save_user_profile(sender, instance, **kwargs):
    """Save a modified user profile

    Parameters
    ----------
    sender : BaseUser
        User creating the new profile
    instance : BaseUser
        Data to be stored in the new user
    """
    if instance.user_type == 1:
        instance.admin.save()
    if instance.user_type == 2:
        instance.faculty.save()
    if instance.user_type == 3:
        instance.student.save()
