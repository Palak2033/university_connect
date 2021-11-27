import json

from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt

from .forms import AnnouncementForm, EditAnnouncementForm
from .models import (
    Announcement,
    Attendance,
    AttendanceReport,
    BaseUser,
    Course,
    Faculty,
    LeaveReport,
    Semester,
    Student,
    StudentResult,
    Subject,
)


def faculty_home(request):
    """Renders the home page for faculty users

    Parameters
    ----------
    request : django.http.HttpRequest
        Client request object. Comes from a HTML template or other function.

    Returns
    -------
    response : django.http.HttpResponse
        Client response object. Goes to a HTML template. Context contains variables used in the frontend
    """
    # Fetching All Student under Faculty
    subjects = Subject.objects.filter(faculty_id=request.user.id)
    subject_count = subjects.count()

    # Fetching All Students under Faculty
    students = Student.objects.none()
    for subject in subjects:
        students |= Student.objects.filter(course_id=subject.course_id)
    students_count = students.count()

    # Fetch All Attendance Count
    attendance_count = Attendance.objects.filter(
        subject_id__in=subjects
    ).count()

    # Fetch All Leave statuses
    leaves = LeaveReport.objects.filter(user=request.user.id)
    leave_count = 1
    for leave in leaves:
        leave_count += (leave.end_date - leave.start_date).days

    context = {
        "students_count": students_count,
        "attendance_count": attendance_count,
        "subject_count": subject_count,
        "leave_count": leave_count,
    }
    return render(
        request, "faculty_templates/faculty_home_template.html", context
    )


def faculty_view_subjects(request):
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
    subjects = Subject.objects.filter(faculty_id=request.user.id).order_by(
        "subject_name"
    )
    context = {"subjects": subjects}
    return render(
        request, "faculty_templates/faculty_view_subjects.html", context
    )


def faculty_view_students(request):
    """Redirects to the view students page

    Parameters
    ----------
    request : django.http.HttpRequest
        Client request object. Comes from a HTML template or other function.

    Returns
    -------
    response : django.http.HttpResponse
        Client response object. Goes to a HTML template. Context contains variables used in the frontend
    """
    subjects = Subject.objects.filter(faculty_id=request.user.id)
    students = Student.objects.none()
    for subject in subjects:
        students |= Student.objects.filter(course_id=subject.course_id)
    students = students.order_by("admin__first_name", "admin__last_name")
    context = {"students": students}
    return render(
        request, "faculty_templates/faculty_view_students.html", context
    )


def faculty_take_attendance(request):
    """Redirects to the take (and view) attendance page

    Parameters
    ----------
    request : django.http.HttpRequest
        Client request object. Comes from a HTML template or other function.

    Returns
    -------
    response : django.http.HttpResponse
        Client response object. Goes to a HTML template. Context contains variables used in the frontend
    """
    subjects = Subject.objects.filter(faculty_id=request.user.id)
    semesters = Semester.objects.all()
    context = {"subjects": subjects, "semesters": semesters}
    return render(
        request, "faculty_templates/take_attendance_template.html", context
    )


def faculty_announcement(request):
    """Redirects to make announcement page

    Parameters
    ----------
    request : django.http.HttpRequest
        Client request object. Comes from a HTML template or other function.

    Returns
    -------
    response : django.http.HttpResponse
        Client response object. Goes to a HTML template. Context contains variables used in the frontend
    """
    form = AnnouncementForm(request.user.id)
    faculty = Faculty.objects.get(admin=request.user.id)
    announcements = Announcement.objects.filter(faculty_id=faculty)
    announcements = reversed(announcements)
    context = {
        "form": form,
        "announcements": announcements,
    }
    return render(
        request,
        "faculty_templates/faculty_announcement_template.html",
        context,
    )


def faculty_announcement_save(request):
    """Takes information from HTML template form and saves new Announcement object

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
        messages.error(request, "Invalid Method.")
        return redirect("faculty_announcement")
    else:
        faculty_obj = Faculty.objects.get(admin=request.user.id)
        form = AnnouncementForm(request.user.id, request.POST, request.FILES)

        if form.is_valid():
            subject_obj = form.cleaned_data["subject_id"]
            message = form.cleaned_data["message"]
            link = form.cleaned_data["link"]

            if len(request.FILES) > 0:
                upload = request.FILES["upload_url"]
                fs = FileSystemStorage()
                filename = fs.save(upload.name, upload)
                upload_url = fs.url(filename)
                upload_name = upload.name
            else:
                upload_url = ""
                upload_name = ""

            try:
                add_announcement = Announcement(
                    faculty_id=faculty_obj,
                    subject_id=subject_obj,
                    message=message,
                    link=link,
                    upload_url=upload_url,
                    upload_name=upload_name,
                )
                add_announcement.save()
                messages.success(request, "Announcement Sent.")
                return redirect("faculty_announcement")
            except Exception as e:
                print(e)

        messages.error(request, "Failed to Send Announcement.")
        return redirect("faculty_announcement")


def faculty_edit_announcement(request, announcement_id):
    """Redirects to the edit announcement page

    Parameters
    ----------
    request : django.http.HttpRequest
        Client request object. Comes from a HTML template or other function.
    announcement_id : int
        Primary key of the announcement in the Announcement table.

    Returns
    -------
    response : django.http.HttpResponse
        Client response object. Goes to a HTML template. Context contains variables used in the frontend
    """
    form = EditAnnouncementForm(request.user.id)
    announcement = Announcement.objects.get(id=announcement_id)
    context = {
        "form": form,
        "announcement": announcement,
    }
    return render(
        request, "faculty_templates/faculty_edit_announcement.html", context
    )


def faculty_edit_announcement_save(request):
    """Edits the selected Announcement object

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
        messages.error(request, "Invalid Method.")
        return redirect("faculty_announcement")
    else:
        form = EditAnnouncementForm(
            request.user.id, request.POST, request.FILES
        )
        announcement_id = request.POST.get("announcement_id")

        if form.is_valid():
            subject_obj = form.cleaned_data["subject_id"]
            message = form.cleaned_data["message"]
            link = form.cleaned_data["link"]

            if len(request.FILES) > 0:
                upload = request.FILES["upload_url"]
                fs = FileSystemStorage()
                filename = fs.save(upload.name, upload)
                upload_url = fs.url(filename)
                upload_name = upload.name
            else:
                upload_url = ""
                upload_name = ""

            try:
                edit_announcement = Announcement.objects.get(
                    id=announcement_id
                )
                edit_announcement.subject_id = (
                    subject_obj
                    if subject_obj is not None
                    else edit_announcement.subject_id
                )
                edit_announcement.message = (
                    message if message != "" else edit_announcement.message
                )
                edit_announcement.link = (
                    link if link != "" else edit_announcement.link
                )
                edit_announcement.upload_url = (
                    upload_url
                    if upload_url != ""
                    else edit_announcement.upload_url
                )
                edit_announcement.upload_name = (
                    upload_name
                    if upload_name != ""
                    else edit_announcement.upload_name
                )
                edit_announcement.save()

                messages.success(request, "Announcement Edited.")
                return redirect("faculty_announcement")
            except Exception as e:
                print(e)

    messages.error(request, "Failed to Edit Announcement.")
    return redirect("faculty_announcement")


def faculty_delete_announcement(request, announcement_id):
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
        return redirect("faculty_announcement")
    except:
        messages.error(request, "Failed to Delete Announcement.")
        return redirect("faculty_announcement")


def faculty_apply_leave(request):
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
        request, "faculty_templates/faculty_apply_leave_template.html", context
    )


def faculty_apply_leave_save(request):
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
        return redirect("faculty_apply_leave")
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
            return redirect("faculty_apply_leave")
        except:
            messages.error(request, "Failed to Apply Leave")
            return redirect("faculty_apply_leave")


def faculty_add_result(request):
    """Redirects to the add result page

    Parameters
    ----------
    request : django.http.HttpRequest
        Client request object. Comes from a HTML template or other function.

    Returns
    -------
    response : django.http.HttpResponse
        Client response object. Goes to a HTML template. Context contains variables used in the frontend
    """
    subjects = Subject.objects.filter(faculty_id=request.user.id)
    semesters = Semester.objects.all()
    results = StudentResult.objects.none()
    for subject in subjects:
        results |= StudentResult.objects.filter(subject_id=subject)
    context = {
        "subjects": subjects,
        "semesters": semesters,
        "results": results,
    }
    return render(
        request, "faculty_templates/add_result_template.html", context
    )


def faculty_add_result_save(request):
    """Takes information from HTML template form and saves new StudentResult object

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
        return redirect("faculty_add_result")
    else:
        student_admin_id = request.POST.get("student_list")
        assignment_marks = request.POST.get("assignment_marks")
        exam_marks = request.POST.get("exam_marks")
        subject_id = request.POST.get("subject")

        student_obj = Student.objects.get(admin=student_admin_id)
        subject_obj = Subject.objects.get(id=subject_id)

        try:
            # Check if Student Result Already Exists or not
            check_exist = StudentResult.objects.filter(
                subject_id=subject_obj, student_id=student_obj
            ).exists()
            if check_exist:
                result = StudentResult.objects.get(
                    subject_id=subject_obj, student_id=student_obj
                )
                result.assignment_marks = assignment_marks
                result.exam_marks = exam_marks
                result.save()
                messages.success(request, "Result Updated Successfully!")
                return redirect("faculty_add_result")
            else:
                result = StudentResult(
                    student_id=student_obj,
                    subject_id=subject_obj,
                    exam_marks=exam_marks,
                    assignment_marks=assignment_marks,
                )
                result.save()
                messages.success(request, "Result Added Successfully!")
                return redirect("faculty_add_result")
        except:
            messages.error(request, "Failed to Add Result!")
            return redirect("faculty_add_result")


# WE don't need csrf_token when using Ajax
@csrf_exempt
def get_students(request):
    """Gets students data for the jQuery graph on the home page

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
    semester = request.POST.get("semester")

    # Student enroll to Course, Course has Subject
    # Getting all data from subject model based on subject_id
    subject_model = Subject.objects.get(id=subject_id)

    semester_model = Semester.objects.get(id=semester)

    students = Student.objects.filter(
        course_id=subject_model.course_id, semester_id=semester_model
    )

    # Only Passing Student Id and Student Name Only
    list_data = []

    for student in students:
        data_small = {
            "id": student.admin.id,
            "name": student.admin.first_name + " " + student.admin.last_name,
        }
        list_data.append(data_small)

    return JsonResponse(
        json.dumps(list_data), content_type="application/json", safe=False
    )


@csrf_exempt
def save_attendance_data(request):
    """Saves student-wise attendance data

    Parameters
    ----------
    request : django.http.HttpRequest
        Client request object. Comes from a HTML template or other function.

    Returns
    -------
    response : django.http.HttpResponse
        Client response object. Goes to a HTML template.
    """
    # Get Values from Staf Take Attendance form via AJAX (JavaScript)
    # Use getlist to access HTML Array/List Input Data
    student_ids = request.POST.get("student_ids")
    subject_id = request.POST.get("subject_id")
    attendance_date = request.POST.get("attendance_date")
    semester_id = request.POST.get("semester_id")

    subject_model = Subject.objects.get(id=subject_id)
    semester_model = Semester.objects.get(id=semester_id)

    json_student = json.loads(student_ids)
    # print(dict_student[0]['id'])

    # print(student_ids)
    try:
        # First Attendance Data is Saved on Attendance Model
        attendance = Attendance(
            subject_id=subject_model,
            attendance_date=attendance_date,
            semester_id=semester_model,
        )
        attendance.save()

        for stud in json_student:
            # Attendance of Individual Student saved on AttendanceReport Model
            student = Student.objects.get(admin=stud["id"])
            attendance_report = AttendanceReport(
                student_id=student,
                attendance_id=attendance,
                status=stud["status"],
            )
            attendance_report.save()
        return HttpResponse("OK")
    except:
        return HttpResponse("Error")


def faculty_update_attendance(request):
    """Redirects to the edit attendance page

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
    subjects = Subject.objects.filter(faculty_id=request.user.id)
    semesters = Semester.objects.all()
    context = {"subjects": subjects, "semesters": semesters}
    return render(
        request, "faculty_templates/update_attendance_template.html", context
    )


@csrf_exempt
def get_attendance_dates(request):
    """Gets subject wise attendance data

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
def get_attendance_student(request):
    """Gets students-wise attendance data

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


@csrf_exempt
def update_attendance_data(request):
    """Updates student-wise attendance data

    Parameters
    ----------
    request : django.http.HttpRequest
        Client request object. Comes from a HTML template or other function.

    Returns
    -------
    response : django.http.HttpResponse
        Client response object. Goes to a HTML template.
    """
    student_ids = request.POST.get("student_ids")

    attendance_date = request.POST.get("attendance_date")
    attendance = Attendance.objects.get(id=attendance_date)

    json_student = json.loads(student_ids)

    try:
        for stud in json_student:
            # Attendance of Individual Student saved on AttendanceReport Model
            student = Student.objects.get(admin=stud["id"])

            attendance_report = AttendanceReport.objects.get(
                student_id=student, attendance_id=attendance
            )
            attendance_report.status = stud["status"]

            attendance_report.save()
        return HttpResponse("OK")
    except:
        return HttpResponse("Error")


def faculty_profile(request):
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
    faculty = Faculty.objects.get(admin=user)

    context = {"user": user, "faculty": faculty}
    return render(request, "faculty_templates/faculty_profile.html", context)


def faculty_profile_update(request):
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
        return redirect("faculty_profile")
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

            faculty = Faculty.objects.get(admin=baseuser.id)
            faculty.address = address
            faculty.save()

            messages.success(request, "Profile Updated Successfully")
            return redirect("faculty_profile")
        except:
            messages.error(request, "Failed to Update Profile")
            return redirect("faculty_profile")
