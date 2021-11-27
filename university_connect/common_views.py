from django.contrib import messages
from django.http.response import HttpResponse
from django.shortcuts import redirect, render

from .models import BaseUser, Feedback, LeaveReport


def delete_leave(request, leave_id):
    """Deletes the selected LeaveReport object permanently

    Parameters
    ----------
    request : django.http.HttpRequest
        Client request object. Comes from a HTML template or other function.
    leave_id : int
        Primary key of the leave report in the LeaveReport table.

    Returns
    -------
    response : django.http.HttpResponse
        Client response object. Goes to a HTML template. Context contains variables used in the frontend
    """
    leave_id = LeaveReport.objects.get(id=leave_id)
    try:
        leave_id.delete()
        messages.success(request, "Leave Request Deleted Successfully.")
        return redirect(request.META.get("HTTP_REFERER"))
    except:
        messages.error(request, "Failed to Delete Leave Request.")
        return redirect(request.META.get("HTTP_REFERER"))


def feedback(request):
    """Upload feedback for admin

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
    feedback_data = Feedback.objects.filter(user=user)
    context = {"feedback_data": feedback_data}

    if user.user_type == "2":
        return render(
            request, "faculty_templates/faculty_feedback.html", context
        )
    elif user.user_type == "3":
        return render(
            request, "student_templates/student_feedback.html", context
        )
    else:
        return HttpResponse("Invalid user type!")


def feedback_save(request):
    """Takes information from HTML template form and saves new Feedback object

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
    else:
        feedback = request.POST.get("feedback_message")
        user = BaseUser.objects.get(id=request.user.id)

        try:
            add_feedback = Feedback(
                user=user, feedback=feedback, feedback_reply=""
            )
            add_feedback.save()
            messages.success(request, "Feedback Sent.")
        except:
            messages.error(request, "Failed to Send Feedback.")

    return redirect(request.META.get("HTTP_REFERER"))
