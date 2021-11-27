import datetime  # To Parse input DateTime into Python Date Time Object

from django.contrib import messages
from django.shortcuts import redirect, render

from .models import (
    Announcement,
    Attendance,
    AttendanceReport,
    BaseUser,
    Course,
    Faculty,
    LeaveReport,
    Student,
    StudentResult,
    Subject,
)


def student_home(request):
    """Renders the home page for student users

    Parameters
    ----------
    request : django.http.HttpRequest
        Client request object. Comes from a HTML template or other function.

    Returns
    -------
    response : django.http.HttpResponse
        Client response object. Goes to a HTML template. Context contains variables used in the frontend
    """
    student_obj = Student.objects.get(admin=request.user.id)
    total_attendance = AttendanceReport.objects.filter(
        student_id=student_obj
    ).count()
    announcements = Announcement.objects.none()
    faculties = Faculty.objects.none()

    course_obj = Course.objects.get(id=student_obj.course_id.id)
    total_subjects = Subject.objects.filter(course_id=course_obj).count()

    subject_name = []
    subject_data = Subject.objects.filter(course_id=student_obj.course_id)
    for subject in subject_data:
        subject_name.append(subject.subject_name)
        announcements |= Announcement.objects.filter(
            subject_id=subject, read_status=False
        )
        faculties |= Faculty.objects.filter(admin=subject.faculty_id)
    
    faculty_count = faculties.count()

    # Fetch All Leave statuses
    leaves = LeaveReport.objects.filter(user=request.user.id)
    leave_count = 0
    for leave in leaves:
        leave_count += (leave.end_date - leave.start_date).days + 1

    # Display only the 3 latest announcements on home page
    non_empty = len(announcements) != 0
    announcements = announcements.order_by("-id")[:3]

    context = {
        "total_attendance": total_attendance,
        "leave_count": leave_count,
        "faculty_count": faculty_count,
        "total_subjects": total_subjects,
        "subject_name": subject_name,
        "announcements": announcements,
        "non_empty": non_empty,
    }
    return render(
        request, "student_templates/student_home_template.html", context
    )


def student_view_subjects(request):
    """Redirects to the view subject page

    Parameters
    ----------
    request : django.http.HttpRequest
        Client request object. Comes from a HTML template or other function.

    Returns
    -------
    response : django.http.HttpResponse
        Client response object. Goes to a HTML template. Context contains variables used in the frontend
    """
    course_id = Student.objects.get(admin=request.user.id).course_id
    subjects = Subject.objects.filter(course_id=course_id)
    context = {"subjects": subjects}
    return render(
        request, "student_templates/student_view_subjects.html", context
    )


def student_view_faculty(request):
    """Redirects to the view faculty page

    Parameters
    ----------
    request : django.http.HttpRequest
        Client request object. Comes from a HTML template or other function.

    Returns
    -------
    response : django.http.HttpResponse
        Client response object. Goes to a HTML template. Context contains variables used in the frontend
    """
    student = Student.objects.get(admin=request.user.id)
    subjects = Subject.objects.filter(course_id=student.course_id)
    faculties = Faculty.objects.none()
    for subject in subjects:
        faculties |= Faculty.objects.filter(admin=subject.faculty_id)
    context = {"faculties": faculties}
    return render(
        request, "student_templates/student_view_faculty.html", context
    )


def student_view_attendance(request):
    """Redirects to the view attendance page

    Parameters
    ----------
    request : django.http.HttpRequest
        Client request object. Comes from a HTML template or other function.

    Returns
    -------
    response : django.http.HttpResponse
        Client response object. Goes to a HTML template. Context contains variables used in the frontend
    """
    student = Student.objects.get(
        admin=request.user.id
    )  # Getting Logged in Student Data
    course = student.course_id  # Getting Course Enrolled of LoggedIn Student
    subjects = Subject.objects.filter(
        course_id=course
    )  # Getting the Subject of Course Enrolled
    context = {"subjects": subjects}
    return render(
        request, "student_templates/student_view_attendance.html", context
    )


def student_view_attendance_post(request):
    """Fetches student attendance data and sends to the jQuery script in the view attendance page

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
        return redirect("student_view_attendance")
    else:
        # Getting all the Input Data
        subject_id = request.POST.get("subject")
        start_date = request.POST.get("start_date")
        end_date = request.POST.get("end_date")

        # Parsing the date data into Python object
        start_date_parse = datetime.datetime.strptime(
            start_date, "%Y-%m-%d"
        ).date()
        end_date_parse = datetime.datetime.strptime(
            end_date, "%Y-%m-%d"
        ).date()

        # Getting all the Subject Data based on Selected Subject
        subject_obj = Subject.objects.get(id=subject_id)
        # Getting Logged In User Data
        user_obj = BaseUser.objects.get(id=request.user.id)
        # Getting Student Data Based on Logged in Data
        stud_obj = Student.objects.get(admin=user_obj)

        # Now Accessing Attendance Data based on the Range of Date Selected and Subject Selected
        attendance = Attendance.objects.filter(
            attendance_date__range=(start_date_parse, end_date_parse),
            subject_id=subject_obj,
        )
        # Getting Attendance Report based on the attendance details obtained above
        attendance_reports = AttendanceReport.objects.filter(
            attendance_id__in=attendance, student_id=stud_obj
        )

        context = {
            "subject_obj": subject_obj,
            "attendance_reports": attendance_reports,
        }

        return render(
            request, "student_templates/student_attendance_data.html", context
        )


def student_announcement(request):
    """Redirects to view announcement page

    Parameters
    ----------
    request : django.http.HttpRequest
        Client request object. Comes from a HTML template or other function.

    Returns
    -------
    response : django.http.HttpResponse
        Client response object. Goes to a HTML template. Context contains variables used in the frontend
    """
    student_obj = Student.objects.get(admin=request.user.id)
    subjects = Subject.objects.filter(course_id=student_obj.course_id)
    announcements = Announcement.objects.none()
    for subject in subjects:
        announcements |= Announcement.objects.filter(subject_id=subject)
    non_empty = len(announcements) != 0

    try:
        unread_announcements = announcements.filter(
            read_status=False
        ).order_by("-updated_at")
        read_announcements = announcements.filter(read_status=True).order_by(
            "-updated_at"
        )

        context = {
            "unread_announcements": unread_announcements,
            "read_announcements": read_announcements,
            "non_empty": non_empty,
        }
        return render(
            request,
            "student_templates/student_announcement_template.html",
            context,
        )
    finally:
        for announcement in unread_announcements:
            announcement.read_status = True
            announcement.save()


def student_apply_leave(request):
    """Redirects to apply leave page

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
    leave_reports = LeaveReport.objects.filter(user=user)
    context = {"leave_reports": leave_reports}
    return render(
        request, "student_templates/student_apply_leave_template.html", context
    )


def student_apply_leave_save(request):
    """Takes information from HTML template form and saves new LeaveReport object

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
    else:
        start_date = request.POST.get("start_date")
        end_date = request.POST.get("end_date")
        message = request.POST.get("message")

        try:
            user = BaseUser.objects.get(id=request.user.id)
            leave_report = LeaveReport(
                user=user,
                start_date=start_date,
                end_date=end_date,
                message=message,
                status=0,
            )
            leave_report.save()
            messages.success(request, "Applied for Leave.")
        except:
            messages.error(request, "Failed to Apply Leave")

    return redirect("student_apply_leave")


def student_view_result(request):
    """Redirects to view results page

    Parameters
    ----------
    request : django.http.HttpRequest
        Client request object. Comes from a HTML template or other function.

    Returns
    -------
    response : django.http.HttpResponse
        Client response object. Goes to a HTML template. Context contains variables used in the frontend
    """
    student = Student.objects.get(admin=request.user.id)
    results = StudentResult.objects.filter(student_id=student.id)
    context = {
        "results": results,
    }
    return render(
        request, "student_templates/view_result_template.html", context
    )


def student_profile(request):
    """Redirects to the edit profile page

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
    student = Student.objects.get(admin=user)

    context = {"user": user, "student": student}
    return render(request, "student_templates/student_profile.html", context)


def student_profile_update(request):
    """Edits the selected student's profile

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
    else:
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        password = request.POST.get("password")
        address = request.POST.get("address")

        try:
            baseuser = BaseUser.objects.get(id=request.user.id)
            baseuser.first_name = first_name
            baseuser.last_name = last_name
            if password != None and password != "":
                baseuser.set_password(password)
            baseuser.save()

            student = Student.objects.get(admin=baseuser.id)
            student.address = address
            student.save()

            messages.success(request, "Profile Updated Successfully")
        except:
            messages.error(request, "Failed to Update Profile")

    return redirect("student_profile")
