from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin


class LoginCheckMiddleWare(MiddlewareMixin):
    """Middleware Class to help with user authentication
    """

    def process_view(self, request, view_func, view_args, view_kwargs):
        """Checks user sessions and makes sure users aren't able to access views they're not allowed to

        Parameters
        ----------
        request : django.http.HttpRequest
            Client request object. Comes from a HTML template or other function.
        view_func : Function
            View function that is being called by the current user
        
        Returns
        -------
        redirect : django.http.HttpResponseRedirect
            Redirects to the page that calls it
        """
        modulename = view_func.__module__
        user = request.user

        # Check whether the user is logged in or not
        if user.is_authenticated:
            if user.user_type == "1":
                if modulename == "university_connect.admin_views":
                    pass
                elif (
                    modulename == "university_connect.views"
                    or modulename == "university_connect.common_views"
                    or modulename == "django.views.static"
                ):
                    pass
                else:
                    return redirect("admin_home")

            elif user.user_type == "2":
                if modulename == "university_connect.faculty_views":
                    pass
                elif (
                    modulename == "university_connect.views"
                    or modulename == "university_connect.common_views"
                    or modulename == "django.views.static"
                ):
                    pass
                else:
                    return redirect("faculty_home")

            elif user.user_type == "3":
                if modulename == "university_connect.student_views":
                    pass
                elif (
                    modulename == "university_connect.views"
                    or modulename == "university_connect.common_views"
                    or modulename == "django.views.static"
                ):
                    pass
                else:
                    return redirect("student_home")

            else:
                return redirect("login")

        else:
            if request.path == reverse("login") or request.path == reverse(
                "doLogin"
            ):
                pass
            else:
                return redirect("login")
