import json

from django.contrib import messages
from django.core import serializers
from django.core.files.storage import FileSystemStorage  # To upload Profile Picture
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from university_connect.forms import AddStudentForm, EditStudentForm
from university_connect.models import (
    Announcement,
    Attendance,
    AttendanceReport,
    BaseUser,
    Course,
    Faculty,
    Feedback,
    LeaveReport,
    Semester,
    Student,
    StudentResult,
    Subject,
)


def admin_home(request):
    """Renders the home page for admin users

    Parameters
    ----------
    request : django.http.HttpRequest
        Client request object. Comes from a HTML template or other function.

    Returns
    -------
    response : django.http.HttpResponse
        Client response object. Goes to a HTML template. Context contains variables used in the frontend
    """
    all_student_count = Student.objects.all().count()
    subject_count = Subject.objects.all().count()
    course_count = Course.objects.all().count()
    faculty_count = Faculty.objects.all().count()

    # Total Subject and students in Each Course
    course_all = Course.objects.all()
    course_name_list = []
    subject_count_list = []
    student_count_list_in_course = []

    for course in course_all:
        subject = Subject.objects.filter(course_id=course.id).count()
        students = Student.objects.filter(course_id=course.id).count()
        course_name_list.append(course.course_name)
        subject_count_list.append(Subject)
        student_count_list_in_course.append(students)

    subject_all = Subject.objects.all()
    subject_list = []
    student_count_list_in_subject = []
    for subject in subject_all:
        course = Course.objects.get(id=subject.course_id.id)
        student_count = Student.objects.filter(course_id=course.id).count()
        subject_list.append(subject.subject_name)
        student_count_list_in_subject.append(student_count)

    # For Faculty
    faculty_attendance_present_list = []
    faculty_name_list = []

    faculties = Faculty.objects.all()
    for faculty in faculties:
        subject_ids = Subject.objects.filter(faculty_id=faculty.admin.id)
        attendance = Attendance.objects.filter(
            subject_id__in=subject_ids
        ).count()
        faculty_attendance_present_list.append(attendance)
        faculty_name_list.append(faculty.admin.first_name)

    # For Student
    student_attendance_present_list = []
    student_name_list = []

    students = Student.objects.all()
    for student in students:
        attendance = AttendanceReport.objects.filter(
            student_id=student.id, status=True
        ).count()
        student_attendance_present_list.append(attendance)
        student_name_list.append(student.admin.first_name)

    # Feedbacks
    feedbacks = Feedback.objects.order_by("-id")[:5]

    context = {
        "all_student_count": all_student_count,
        "subject_count": subject_count,
        "course_count": course_count,
        "faculty_count": faculty_count,
        "course_name_list": course_name_list,
        "subject_count_list": subject_count_list,
        "student_count_list_in_course": student_count_list_in_course,
        "subject_list": subject_list,
        "student_count_list_in_subject": student_count_list_in_subject,
        "faculty_attendance_present_list": faculty_attendance_present_list,
        "faculty_name_list": faculty_name_list,
        "student_attendance_present_list": student_attendance_present_list,
        "student_name_list": student_name_list,
        "feedbacks": feedbacks,
    }
    return render(request, "admin_templates/home_content.html", context)


def add_faculty(request):
    """Redirects to the add faculty page

    Parameters
    ----------
    request : django.http.HttpRequest
        Client request object. Comes from a HTML template or other function.

    Returns
    -------
    response : django.http.HttpResponse
        Client response object. Goes to a HTML template. Context contains variables used in the frontend
    """
    return render(request, "admin_templates/add_faculty_template.html")


def add_faculty_save(request):
    """Takes information from HTML template form and saves new Faculty object

    Parameters
    ----------
    request : django.http.HttpRequest
        Client request object. Comes from a HTML template or other function.

    Returns
    -------
    redirect : django.http.HttpResponseRedirect
        Redirects to the page that calls it
    """
    if request.method != "POST":
        messages.error(request, "Invalid Method ")
        return redirect("add_faculty")
    else:
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        address = request.POST.get("address")

        try:
            user = BaseUser.objects.create_user(
                username=username,
                password=password,
                email=email,
                first_name=first_name,
                last_name=last_name,
                user_type=2,
            )
            user.faculty.address = address
            user.save()
            messages.success(request, "Faculty Added Successfully!")
            return redirect("add_faculty")
        except Exception as e:
            print(e)
            messages.error(request, "Failed to Add Faculty!")
            return redirect("add_faculty")


def manage_faculty(request):
    """Redirects to the manage faculty page

    Parameters
    ----------
    request : django.http.HttpRequest
        Client request object. Comes from a HTML template or other function.

    Returns
    -------
    response : django.http.HttpResponse
        Client response object. Goes to a HTML template. Context contains variables used in the frontend
    """
    faculties = Faculty.objects.all().order_by(
        "admin__first_name", "admin__last_name"
    )
    context = {"faculties": faculties}
    return render(
        request, "admin_templates/manage_faculty_template.html", context
    )


def edit_faculty(request, faculty_id):
    """Redirects to the edit faculty page

    Parameters
    ----------
    request : django.http.HttpRequest
        Client request object. Comes from a HTML template or other function.
    faculty_id : int
        Primary key of the faculty in the BaseUser table.

    Returns
    -------
    response : django.http.HttpResponse
        Client response object. Goes to a HTML template. Context contains variables used in the frontend
    """
    faculty = Faculty.objects.get(admin=faculty_id)
    context = {"faculty": faculty, "id": faculty_id}
    return render(
        request, "admin_templates/edit_faculty_template.html", context
    )


def edit_faculty_save(request):
    """Edits the selected Faculty object

    Parameters
    ----------
    request : django.http.HttpRequest
        Client request object. Comes from a HTML template or other function.

    Returns
    -------
    redirect : django.http.HttpResponseRedirect
        Redirects to the page that calls it
    """
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        faculty_id = request.POST.get("faculty_id")
        username = request.POST.get("username")
        email = request.POST.get("email")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        address = request.POST.get("address")

        try:
            # INSERTING into Base User Model
            user = BaseUser.objects.get(id=faculty_id)
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.username = username
            user.save()

            # INSERTING into Faculty Model
            faculty_model = Faculty.objects.get(admin=faculty_id)
            faculty_model.address = address
            faculty_model.save()

            messages.success(request, "Faculty Updated Successfully.")
            return redirect("/edit_faculty/" + faculty_id)

        except:
            messages.error(request, "Failed to Update Faculty.")
            return redirect("/edit_faculty/" + faculty_id)


def delete_faculty(request, faculty_id):
    """Deletes the selected Faculty object permanently

    Parameters
    ----------
    request : django.http.HttpRequest
        Client request object. Comes from a HTML template or other function.
    faculty_id : int
        Primary key of the faculty in the BaseUser table.

    Returns
    -------
    response : django.http.HttpResponse
        Client response object. Goes to a HTML template. Context contains variables used in the frontend
    """
    faculty = Faculty.objects.get(admin=faculty_id)
    try:
        faculty.delete()
        messages.success(request, "Faculty Deleted Successfully.")
        return redirect("manage_faculty")
    except:
        messages.error(request, "Failed to Delete Faculty.")
        return redirect("manage_faculty")


def add_course(request):
    """Redirects to the add course page

    Parameters
    ----------
    request : django.http.HttpRequest
        Client request object. Comes from a HTML template or other function.

    Returns
    -------
    response : django.http.HttpResponse
        Client response object. Goes to a HTML template. Context contains variables used in the frontend
    """
    return render(request, "admin_templates/add_course_template.html")


def add_course_save(request):
    """Takes information from HTML template form and saves new Course object

    Parameters
    ----------
    request : django.http.HttpRequest
        Client request object. Comes from a HTML template or other function.

    Returns
    -------
    redirect : django.http.HttpResponseRedirect
        Redirects to the page that calls it
    """
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect("add_course")
    else:
        course = request.POST.get("course")
        try:
            course_model = Course(course_name=course)
            course_model.save()
            messages.success(request, "Course Added Successfully!")
            return redirect("add_course")
        except:
            messages.error(request, "Failed to Add Course!")
            return redirect("add_course")


def manage_course(request):
    """Redirects to the manage course page

    Parameters
    ----------
    request : django.http.HttpRequest
        Client request object. Comes from a HTML template or other function.

    Returns
    -------
    response : django.http.HttpResponse
        Client response object. Goes to a HTML template. Context contains variables used in the frontend
    """
    courses = Course.objects.all().order_by("course_name")
    context = {"courses": courses}
    return render(
        request, "admin_templates/manage_course_template.html", context
    )


def edit_course(request, course_id):
    """Edits the selected Course object

    Parameters
    ----------
    request : django.http.HttpRequest
        Client request object. Comes from a HTML template or other function.
    course_id : int
        Primary key of the course in the Course table.

    Returns
    -------
    response : django.http.HttpResponse
        Client response object. Goes to a HTML template. Context contains variables used in the frontend
    """
    course = Course.objects.get(id=course_id)
    context = {"course": course, "id": course_id}
    return render(
        request, "admin_templates/edit_course_template.html", context
    )


def edit_course_save(request):
    """Edits the selected Course object

    Parameters
    ----------
    request : django.http.HttpRequest
        Client request object. Comes from a HTML template or other function.

    Returns
    -------
    redirect : django.http.HttpResponseRedirect
        Redirects to the page that calls it
    """
    if request.method != "POST":
        HttpResponse("Invalid Method")
    else:
        course_id = request.POST.get("course_id")
        course_name = request.POST.get("course")

        try:
            course = Course.objects.get(id=course_id)
            course.course_name = course_name
            course.save()

            messages.success(request, "Course Updated Successfully.")
            return redirect("manage_course")

        except:
            messages.error(request, "Failed to Update Course.")
            return redirect("manage_course")


def delete_course(request, course_id):
    """Deletes the selected Course object permanently

    Parameters
    ----------
    request : django.http.HttpRequest
        Client request object. Comes from a HTML template or other function.
    course_id : int
        Primary key of the course in the Course table.

    Returns
    -------
    response : django.http.HttpResponse
        Client response object. Goes to a HTML template. Context contains variables used in the frontend
    """
    course = Course.objects.get(id=course_id)
    try:
        course.delete()
        messages.success(request, "Course Deleted Successfully.")
        return redirect("manage_course")
    except:
        messages.error(request, "Failed to Delete Course.")
        return redirect("manage_course")


def manage_semester(request):
    """Redirects to the manage semester page

    Parameters
    ----------
    request : django.http.HttpRequest
        Client request object. Comes from a HTML template or other function.

    Returns
    -------
    response : django.http.HttpResponse
        Client response object. Goes to a HTML template. Context contains variables used in the frontend
    """
    semesters = Semester.objects.all().order_by("start_year")
    context = {"semesters": semesters}
    return render(
        request, "admin_templates/manage_semester_template.html", context
    )


def add_semester(request):
    """Redirects to the add semester page

    Parameters
    ----------
    request : django.http.HttpRequest
        Client request object. Comes from a HTML template or other function.

    Returns
    -------
    response : django.http.HttpResponse
        Client response object. Goes to a HTML template. Context contains variables used in the frontend
    """
    return render(request, "admin_templates/add_semester_template.html")


def add_semester_save(request):
    """Takes information from HTML template form and saves new Semester object

    Parameters
    ----------
    request : django.http.HttpRequest
        Client request object. Comes from a HTML template or other function.

    Returns
    -------
    redirect : django.http.HttpResponseRedirect
        Redirects to the page that calls it
    """
    if request.method != "POST":
        messages.error(request, "Invalid Method")
        return redirect("add_course")
    else:
        start_year = request.POST.get("start_year")
        end_year = request.POST.get("end_year")

        try:
            semester = Semester(start_year=start_year, end_year=end_year)
            semester.save()
            messages.success(request, "Semester added Successfully!")
            return redirect("add_semester")
        except:
            messages.error(request, "Failed to Add Semester")
            return redirect("add_semester")


def edit_semester(request, semester_id):
    """Redirects to the edit semester page

    Parameters
    ----------
    request : django.http.HttpRequest
        Client request object. Comes from a HTML template or other function.
    semester_id : int
        Primary key of the semester in the Semester table.

    Returns
    -------
    response : django.http.HttpResponse
        Client response object. Goes to a HTML template. Context contains variables used in the frontend
    """
    semester = Semester.objects.get(id=semester_id)
    context = {"semester": semester}
    return render(
        request, "admin_templates/edit_semester_template.html", context
    )


def edit_semester_save(request):
    """Edits the selected Semester object

    Parameters
    ----------
    request : django.http.HttpRequest
        Client request object. Comes from a HTML template or other function.

    Returns
    -------
    redirect : django.http.HttpResponseRedirect
        Redirects to the page that calls it
    """
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect("manage_semester")
    else:
        semester_id = request.POST.get("semester_id")
        start_year = request.POST.get("start_year")
        end_year = request.POST.get("end_year")

        try:
            semester = Semester.objects.get(id=semester_id)
            semester.start_year = start_year
            semester.end_year = end_year
            semester.save()

            messages.success(request, "Semester Updated Successfully.")
            return redirect("/edit_semester/" + semester_id)
        except:
            messages.error(request, "Failed to Update Semester.")
            return redirect("/edit_semester/" + semester_id)


def delete_semester(request, semester_id):
    """Deletes the selected Semester object permanently

    Parameters
    ----------
    request : django.http.HttpRequest
        Client request object. Comes from a HTML template or other function.
    semester_id : int
        Primary key of the semester in the Semester table.

    Returns
    -------
    response : django.http.HttpResponse
        Client response object. Goes to a HTML template. Context contains variables used in the frontend
    """
    semester = Semester.objects.get(id=semester_id)
    try:
        semester.delete()
        messages.success(request, "Semester Deleted Successfully.")
        return redirect("manage_semester")
    except:
        messages.error(request, "Failed to Delete Semester.")
        return redirect("manage_semester")


def add_student(request):
    """Redirects to the add student page

    Parameters
    ----------
    request : django.http.HttpRequest
        Client request object. Comes from a HTML template or other function.

    Returns
    -------
    response : django.http.HttpResponse
        Client response object. Goes to a HTML template. Context contains variables used in the frontend
    """
    form = AddStudentForm()
    context = {"form": form}
    return render(
        request, "admin_templates/add_student_template.html", context
    )


def add_student_save(request):
    """Takes information from HTML template form and saves new Student object

    Parameters
    ----------
    request : django.http.HttpRequest
        Client request object. Comes from a HTML template or other function.

    Returns
    -------
    redirect : django.http.HttpResponseRedirect
        Redirects to the page that calls it
    """
    if request.method != "POST":
        messages.error(request, "Invalid Method")
        return redirect("add_student")
    else:
        form = AddStudentForm(request.POST, request.FILES)

        if form.is_valid():
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]
            username = form.cleaned_data["username"]
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            address = form.cleaned_data["address"]
            semester_id = form.cleaned_data["semester_id"]
            course_id = form.cleaned_data["course_id"]
            gender = form.cleaned_data["gender"]

            # Getting Profile Pic first
            # First Check whether the file is selected or not
            # Upload only if file is selected
            if len(request.FILES) != 0:
                profile_pic = request.FILES["profile_pic"]
                fs = FileSystemStorage()
                filename = fs.save(profile_pic.name, profile_pic)
                profile_pic_url = fs.url(filename)
            else:
                profile_pic_url = None

            try:
                user = BaseUser.objects.create_user(
                    username=username,
                    password=password,
                    email=email,
                    first_name=first_name,
                    last_name=last_name,
                    user_type=3,
                )
                user.student.address = address

                course_obj = Course.objects.get(id=course_id)
                user.student.course_id = course_obj

                semester_obj = Semester.objects.get(id=semester_id)
                user.student.semester_id = semester_obj

                user.student.gender = gender
                user.student.profile_pic = profile_pic_url
                user.save()
                messages.success(request, "Student Added Successfully!")
                return redirect("add_student")
            except:
                messages.error(request, "Failed to Add Student!")
                return redirect("add_student")
        else:
            return redirect("add_student")


def manage_student(request):
    """Redirects to the manage student page

    Parameters
    ----------
    request : django.http.HttpRequest
        Client request object. Comes from a HTML template or other function.

    Returns
    -------
    response : django.http.HttpResponse
        Client response object. Goes to a HTML template. Context contains variables used in the frontend
    """
    students = Student.objects.all().order_by(
        "admin__first_name", "admin__last_name"
    )
    context = {"students": students}
    return render(
        request, "admin_templates/manage_student_template.html", context
    )


def edit_student(request, student_id):
    """Edits the selected Semester object

    Parameters
    ----------
    request : django.http.HttpRequest
        Client request object. Comes from a HTML template or other function.
    student_id : int
        Primary key of the student in the Student table.

    Returns
    -------
    response : django.http.HttpResponse
        Client response object. Goes to a HTML template. Context contains variables used in the frontend
    """
    # Adding Student ID into Session Variable
    request.session["student_id"] = student_id

    student = Student.objects.get(admin=student_id)
    form = EditStudentForm()
    # Filling the form with Data from Database
    form.fields["email"].initial = student.admin.email
    form.fields["username"].initial = student.admin.username
    form.fields["first_name"].initial = student.admin.first_name
    form.fields["last_name"].initial = student.admin.last_name
    form.fields["address"].initial = student.address
    form.fields["course_id"].initial = student.course_id.id
    form.fields["gender"].initial = student.gender
    form.fields["semester_id"].initial = student.semester_id.id

    context = {
        "id": student_id,
        "username": student.admin.username,
        "form": form,
    }
    return render(
        request, "admin_templates/edit_student_template.html", context
    )


def edit_student_save(request):
    """Edits the selected Student object

    Parameters
    ----------
    request : django.http.HttpRequest
        Client request object. Comes from a HTML template or other function.

    Returns
    -------
    redirect : django.http.HttpResponseRedirect
        Redirects to the page that calls it
    """
    if request.method != "POST":
        return HttpResponse("Invalid Method!")
    else:
        student_id = request.session.get("student_id")
        if student_id == None:
            return redirect("/manage_student")

        form = EditStudentForm(request.POST, request.FILES)
        if form.is_valid():
            email = form.cleaned_data["email"]
            username = form.cleaned_data["username"]
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]
            address = form.cleaned_data["address"]
            course_id = form.cleaned_data["course_id"]
            gender = form.cleaned_data["gender"]
            semester_id = form.cleaned_data["semester_id"]

            # Getting Profile Pic first
            # First Check whether the file is selected or not
            # Upload only if file is selected
            if len(request.FILES) != 0:
                profile_pic = request.FILES["profile_pic"]
                fs = FileSystemStorage()
                filename = fs.save(profile_pic.name, profile_pic)
                profile_pic_url = fs.url(filename)
            else:
                profile_pic_url = None

            try:
                # First Update into Custom User Model
                user = BaseUser.objects.get(id=student_id)
                user.first_name = first_name
                user.last_name = last_name
                user.email = email
                user.username = username
                user.save()

                # Then Update Student Table
                student_model = Student.objects.get(admin=student_id)
                student_model.address = address

                course = Course.objects.get(id=course_id)
                student_model.course_id = course

                semester_obj = Semester.objects.get(id=semester_id)
                student_model.semester_id = semester_obj

                student_model.gender = gender
                if profile_pic_url != None:
                    student_model.profile_pic = profile_pic_url
                student_model.save()
                # Delete student_id SESSION after the data is updated
                del request.session["student_id"]

                messages.success(request, "Student Updated Successfully!")
                return redirect("/edit_student/" + student_id)
            except:
                messages.success(request, "Failed to Uupdate Student.")
                return redirect("/edit_student/" + student_id)
        else:
            return redirect("/edit_student/" + student_id)


def delete_student(request, student_id):
    """Deletes the selected Student object permanently

    Parameters
    ----------
    request : django.http.HttpRequest
        Client request object. Comes from a HTML template or other function.

    Returns
    -------
    redirect : django.http.HttpResponseRedirect
        Redirects to the page that calls it
    """
    student = Student.objects.get(admin=student_id)
    try:
        student.delete()
        messages.success(request, "Student Deleted Successfully.")
        return redirect("manage_student")
    except:
        messages.error(request, "Failed to Delete Student.")
        return redirect("manage_student")


def add_subject(request):
    """Redirects to the add subject page

    Parameters
    ----------
    request : django.http.HttpRequest
        Client request object. Comes from a HTML template or other function.

    Returns
    -------
    response : django.http.HttpResponse
        Client response object. Goes to a HTML template. Context contains variables used in the frontend
    """
    courses = Course.objects.all()
    faculties = BaseUser.objects.filter(user_type="2")
    context = {"courses": courses, "faculties": faculties}
    return render(
        request, "admin_templates/add_subject_template.html", context
    )


def add_subject_save(request):
    """Takes information from HTML template form and saves new Subject object

    Parameters
    ----------
    request : django.http.HttpRequest
        Client request object. Comes from a HTML template or other function.

    Returns
    -------
    redirect : django.http.HttpResponseRedirect
        Redirects to the page that calls it
    """
    if request.method != "POST":
        messages.error(request, "Method Not Allowed!")
        return redirect("add_subject")
    else:
        subject_name = request.POST.get("subject")

        course_id = request.POST.get("course")
        course = Course.objects.get(id=course_id)

        faculty_id = request.POST.get("faculty")
        faculty = BaseUser.objects.get(id=faculty_id)

        try:
            subject = Subject(
                subject_name=subject_name, course_id=course, faculty_id=faculty
            )
            subject.save()
            messages.success(request, "Subject Added Successfully!")
            return redirect("add_subject")
        except:
            messages.error(request, "Failed to Add Subject!")
            return redirect("add_subject")


def manage_subject(request):
    """Redirects to the manage subject page

    Parameters
    ----------
    request : django.http.HttpRequest
        Client request object. Comes from a HTML template or other function.

    Returns
    -------
    response : django.http.HttpResponse
        Client response object. Goes to a HTML template. Context contains variables used in the frontend
    """
    subjects = Subject.objects.all().order_by("subject_name")
    context = {"subjects": subjects}
    return render(
        request, "admin_templates/manage_subject_template.html", context
    )


def edit_subject(request, subject_id):
    """Redirects to the edit subject page

    Parameters
    ----------
    request : django.http.HttpRequest
        Client request object. Comes from a HTML template or other function.
    subject_id : int
        Primary key of the subject in the Subject table.

    Returns
    -------
    response : django.http.HttpResponse
        Client response object. Goes to a HTML template. Context contains variables used in the frontend
    """
    subject = Subject.objects.get(id=subject_id)
    courses = Course.objects.all()
    faculties = BaseUser.objects.filter(user_type="2")
    context = {
        "subject": subject,
        "courses": courses,
        "faculties": faculties,
    }
    return render(
        request, "admin_templates/edit_subject_template.html", context
    )


def edit_subject_save(request):
    """Edits the selected Subject object

    Parameters
    ----------
    request : django.http.HttpRequest
        Client request object. Comes from a HTML template or other function.

    Returns
    -------
    redirect : django.http.HttpResponseRedirect
        Redirects to the page that calls it
    """
    if request.method != "POST":
        HttpResponse("Invalid Method.")
    else:
        subject_id = request.POST.get("subject_id")
        subject_name = request.POST.get("subject")
        course_id = request.POST.get("course")
        faculty_id = request.POST.get("faculty")

        try:
            subject = Subject.objects.get(id=subject_id)
            subject.subject_name = (
                subject_name if subject_name != "" else subject.subject_name
            )

            course = Course.objects.get(id=course_id)
            subject.course_id = course

            faculty = BaseUser.objects.get(id=faculty_id)
            subject.faculty_id = faculty

            subject.save()

            messages.success(request, "Subject Updated Successfully.")
            # return redirect('/edit_subject/'+subject_id)
            return HttpResponseRedirect(
                reverse("edit_subject", kwargs={"subject_id": subject_id})
            )

        except:
            messages.error(request, "Failed to Update Subject.")
            return HttpResponseRedirect(
                reverse("edit_subject", kwargs={"subject_id": subject_id})
            )
            # return redirect('/edit_subject/'+subject_id)


def delete_subject(request, subject_id):
    """Deletes the selected Subject object permanently

    Parameters
    ----------
    request : django.http.HttpRequest
        Client request object. Comes from a HTML template or other function.
    subject_id : int
        Primary key of the subject in the Subject table.

    Returns
    -------
    redirect : django.http.HttpResponseRedirect
        Redirects to the page that calls it
    """
    subject = Subject.objects.get(id=subject_id)
    try:
        subject.delete()
        messages.success(request, "Subject Deleted Successfully.")
        return redirect("manage_subject")
    except:
        messages.error(request, "Failed to Delete Subject.")
        return redirect("manage_subject")


def manage_leave(request):
    """Redirects to the manage leave page

    Parameters
    ----------
    request : django.http.HttpRequest
        Client request object. Comes from a HTML template or other function.

    Returns
    -------
    response : django.http.HttpResponse
        Client response object. Goes to a HTML template. Context contains variables used in the frontend
    """
    leave_reports = LeaveReport.objects.all()
    context = {"leave_reports": leave_reports}
    return render(
        request, "admin_templates/manage_leave_template.html", context
    )


def change_leave(request, leave_id, status):
    """Redirects to the change leave page

    Parameters
    ----------
    request : django.http.HttpRequest
        Client request object. Comes from a HTML template or other function.
    leave_id : int
        Primary key of the leave report in the LeaveReport table.
    status : int
        Represents current status of leave report. 0 for pending, 1 for approved and 2 for rejected

    Returns
    -------
    response : django.http.HttpResponse
        Client response object. Goes to a HTML template. Context contains variables used in the frontend
    """
    leave_report = LeaveReport.objects.get(id=leave_id)
    leave_report.status = status
    leave_report.save()
    return redirect("manage_leave")


def admin_view_result(request):
    """Redirects to the view results page

    Parameters
    ----------
    request : django.http.HttpRequest
        Client request object. Comes from a HTML template or other function.

    Returns
    -------
    response : django.http.HttpResponse
        Client response object. Goes to a HTML template. Context contains variables used in the frontend
    """
    results = StudentResult.objects.all()
    context = {"results": results}
    return render(
        request, "admin_templates/view_result_template.html", context
    )


@csrf_exempt
def check_email_exist(request):
    """Checks if a given email exists in the user database

    Parameters
    ----------
    request : django.http.HttpRequest
        Client request object. Comes from a HTML template or other function.

    Returns
    -------
    response : django.http.HttpResponse
        Client response object. Goes to a HTML template. Context contains variables used in the frontend
    """
    email = request.POST.get("email")
    user_obj = BaseUser.objects.filter(email=email).exists()
    if user_obj:
        return HttpResponse(True)
    else:
        return HttpResponse(False)


@csrf_exempt
def check_username_exist(request):
    """Checks if the given username exists in the user database

    Parameters
    ----------
    request : django.http.HttpRequest
        Client request object. Comes from a HTML template or other function.

    Returns
    -------
    response : django.http.HttpResponse
        Client response object. Goes to a HTML template. Context contains variables used in the frontend
    """
    username = request.POST.get("username")
    user_obj = BaseUser.objects.filter(username=username).exists()
    if user_obj:
        return HttpResponse(True)
    else:
        return HttpResponse(False)


def feedback_message(request):
    """Redirects to the view feedback page

    Parameters
    ----------
    request : django.http.HttpRequest
        Client request object. Comes from a HTML template or other function.

    Returns
    -------
    response : django.http.HttpResponse
        Client response object. Goes to a HTML template. Context contains variables used in the frontend
    """
    feedbacks = Feedback.objects.all()
    feedbacks = reversed(feedbacks)
    context = {"feedbacks": feedbacks}
    return render(request, "admin_templates/feedback_template.html", context)


@csrf_exempt
def feedback_message_reply(request):
    """Opens window to reply to feedback

    Parameters
    ----------
    request : django.http.HttpRequest
        Client request object. Comes from a HTML template or other function.

    Returns
    -------
    response : django.http.HttpResponse
        Client response object. Goes to a HTML template. Context contains variables used in the frontend
    """
    feedback_id = request.POST.get("id")
    feedback_reply = request.POST.get("reply")

    try:
        feedback = Feedback.objects.get(id=feedback_id)
        feedback.feedback_reply = feedback_reply
        feedback.save()
        return HttpResponse("True")
    except Exception as e:
        print(e)
        return HttpResponse("False")


def admin_announcement(request):
    """Redirects to the view announcements page

    Parameters
    ----------
    request : django.http.HttpRequest
        Client request object. Comes from a HTML template or other function.

    Returns
    -------
    response : django.http.HttpResponse
        Client response object. Goes to a HTML template. Context contains variables used in the frontend
    """
    subjects = Subject.objects.all()
    announcements = Announcement.objects.all()
    non_empty = len(announcements) != 0
    context = {
        "announcements": announcements,
        "subject": subjects,
        "non_empty": non_empty,
    }
    return render(
        request, "admin_templates/announcement_template.html", context
    )


def admin_delete_announcement(request, announcement_id):
    """Deletes the selected Announcement object permanently

    Parameters
    ----------
    request : django.http.HttpRequest
        Client request object. Comes from a HTML template or other function.
    announcement_id : int
        Primary key of the announcement in the Announcement table.

    Returns
    -------
    redirect : django.http.HttpResponseRedirect
        Redirects to the page that calls it
    """
    try:
        delete_announcement = Announcement.objects.filter(id=announcement_id)
        delete_announcement.delete()
        messages.success(request, "Announcement Deleted.")
        return redirect("admin_announcement")
    except:
        messages.error(request, "Failed to Delete Announcement.")
        return redirect("admin_announcement")


def admin_view_attendance(request):
    """Redirects to view attendance page

    Parameters
    ----------
    request : django.http.HttpRequest
        Client request object. Comes from a HTML template or other function.

    Returns
    -------
    response : django.http.HttpResponse
        Client response object. Goes to a HTML template. Context contains variables used in the frontend
    """
    subjects = Subject.objects.all()
    semesters = Semester.objects.all()
    context = {"subjects": subjects, "semesters": semesters}
    return render(
        request, "admin_templates/admin_view_attendance.html", context
    )


@csrf_exempt
def admin_get_attendance_dates(request):
    """Fetches attendance data for the jQuery graph on home page

    Parameters
    ----------
    request : django.http.HttpRequest
        Client request object. Comes from a HTML template or other function.

    Returns
    -------
    response : django.http.JsonResponse
        Client response object. Goes to a JSON template.
    """
    # Getting Values from Ajax POST 'Fetch Student'
    subject_id = request.POST.get("subject")
    semester = request.POST.get("semester_id")

    # Student enroll to Course, Course has Subject
    # Getting all data from subject model based on subject_id
    subject_model = Subject.objects.get(id=subject_id)

    semester_model = Semester.objects.get(id=semester)

    # students = Student.objects.filter(course_id=subject_model.course_id, semester_id=semester_model)
    attendance = Attendance.objects.filter(
        subject_id=subject_model, semester_id=semester_model
    )

    # Only Passing Student Id and Student Name Only
    list_data = []

    for attendance_single in attendance:
        data_small = {
            "id": attendance_single.id,
            "attendance_date": str(attendance_single.attendance_date),
            "semester_id": semester,
        }
        list_data.append(data_small)

    return JsonResponse(
        json.dumps(list_data), content_type="application/json", safe=False
    )


@csrf_exempt
def admin_get_attendance_student(request):
    """Gets student-wise attendance data for the jQuery graph on the home page

    Parameters
    ----------
    request : django.http.HttpRequest
        Client request object. Comes from a HTML template or other function.

    Returns
    -------
    response : django.http.JsonResponse
        Client response object. Goes to a JSON template.
    """
    # Getting Values from Ajax POST 'Fetch Student'
    attendance_date = request.POST.get("attendance_date")
    attendance = Attendance.objects.get(id=attendance_date)

    attendance_data = AttendanceReport.objects.filter(attendance_id=attendance)
    # Only Passing Student Id and Student Name Only
    list_data = []

    for student in attendance_data:
        data_small = {
            "id": student.student_id.admin.id,
            "name": student.student_id.admin.first_name
            + " "
            + student.student_id.admin.last_name,
            "status": student.status,
        }
        list_data.append(data_small)

    return JsonResponse(
        json.dumps(list_data), content_type="application/json", safe=False
    )


def admin_profile(request):
    """Redirects to the admin profile page

    Parameters
    ----------
    request : django.http.HttpRequest
        Client request object. Comes from a HTML template or other function.

    Returns
    -------
    response : django.http.HttpResponse
        Client response object. Goes to a HTML template. Context contains variables used in the frontend
    """
    user = BaseUser.objects.get(id=request.user.id)

    context = {"user": user}
    return render(request, "admin_templates/admin_profile.html", context)


def admin_profile_update(request):
    """Redirects to the profile update page

    Parameters
    ----------
    request : django.http.HttpRequest
        Client request object. Comes from a HTML template or other function.

    Returns
    -------
    redirect : django.http.HttpResponseRedirect
        Redirects to the page that calls it
    """
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect("admin_profile")
    else:
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        password = request.POST.get("password")

        try:
            baseuser = BaseUser.objects.get(id=request.user.id)
            baseuser.first_name = first_name
            baseuser.last_name = last_name
            if password != None and password != "":
                baseuser.set_password(password)
            baseuser.save()
            messages.success(request, "Profile Updated Successfully")
            return redirect("admin_profile")
        except:
            messages.error(request, "Failed to Update Profile")
            return redirect("admin_profile")
