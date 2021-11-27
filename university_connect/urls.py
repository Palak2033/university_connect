from django.urls import path

from . import admin_views, common_views, faculty_views, student_views, views

urlpatterns = [
    path("", views.loginPage, name="login"),
    # path(r'accounts/', include('django.contrib.auth.urls')),
    path("doLogin/", views.doLogin, name="doLogin"),
    path("get_user_details/", views.get_user_details, name="get_user_details"),
    path("logout_user/", views.logout_user, name="logout_user"),
    # URLs for Admin
    path("admin_home/", admin_views.admin_home, name="admin_home"),
    path("add_faculty/", admin_views.add_faculty, name="add_faculty"),
    path(
        "add_faculty_save/",
        admin_views.add_faculty_save,
        name="add_faculty_save",
    ),
    path("manage_faculty/", admin_views.manage_faculty, name="manage_faculty"),
    path(
        "edit_faculty/<faculty_id>/",
        admin_views.edit_faculty,
        name="edit_faculty",
    ),
    path(
        "edit_faculty_save/",
        admin_views.edit_faculty_save,
        name="edit_faculty_save",
    ),
    path(
        "delete_faculty/<faculty_id>/",
        admin_views.delete_faculty,
        name="delete_faculty",
    ),
    path("add_course/", admin_views.add_course, name="add_course"),
    path(
        "add_course_save/", admin_views.add_course_save, name="add_course_save"
    ),
    path("manage_course/", admin_views.manage_course, name="manage_course"),
    path(
        "edit_course/<course_id>/", admin_views.edit_course, name="edit_course"
    ),
    path(
        "edit_course_save/",
        admin_views.edit_course_save,
        name="edit_course_save",
    ),
    path(
        "delete_course/<course_id>/",
        admin_views.delete_course,
        name="delete_course",
    ),
    path(
        "manage_semester/", admin_views.manage_semester, name="manage_semester"
    ),
    path("add_semester/", admin_views.add_semester, name="add_semester"),
    path(
        "add_semester_save/",
        admin_views.add_semester_save,
        name="add_semester_save",
    ),
    path(
        "edit_semester/<semester_id>",
        admin_views.edit_semester,
        name="edit_semester",
    ),
    path(
        "edit_semester_save/",
        admin_views.edit_semester_save,
        name="edit_semester_save",
    ),
    path(
        "delete_semester/<semester_id>/",
        admin_views.delete_semester,
        name="delete_semester",
    ),
    path("add_student/", admin_views.add_student, name="add_student"),
    path(
        "add_student_save/",
        admin_views.add_student_save,
        name="add_student_save",
    ),
    path(
        "edit_student/<student_id>",
        admin_views.edit_student,
        name="edit_student",
    ),
    path(
        "edit_student_save/",
        admin_views.edit_student_save,
        name="edit_student_save",
    ),
    path("manage_student/", admin_views.manage_student, name="manage_student"),
    path(
        "delete_student/<student_id>/",
        admin_views.delete_student,
        name="delete_student",
    ),
    path("add_subject/", admin_views.add_subject, name="add_subject"),
    path(
        "add_subject_save/",
        admin_views.add_subject_save,
        name="add_subject_save",
    ),
    path("manage_subject/", admin_views.manage_subject, name="manage_subject"),
    path(
        "edit_subject/<subject_id>/",
        admin_views.edit_subject,
        name="edit_subject",
    ),
    path(
        "edit_subject_save/",
        admin_views.edit_subject_save,
        name="edit_subject_save",
    ),
    path(
        "delete_subject/<subject_id>/",
        admin_views.delete_subject,
        name="delete_subject",
    ),
    path(
        "check_email_exist/",
        admin_views.check_email_exist,
        name="check_email_exist",
    ),
    path(
        "check_username_exist/",
        admin_views.check_username_exist,
        name="check_username_exist",
    ),
    path(
        "feedback_message/",
        admin_views.feedback_message,
        name="feedback_message",
    ),
    path(
        "feedback_message_reply/",
        admin_views.feedback_message_reply,
        name="feedback_message_reply",
    ),
    path(
        "admin_announcement/",
        admin_views.admin_announcement,
        name="admin_announcement",
    ),
    path(
        "admin_delete_announcement/<announcement_id>",
        admin_views.admin_delete_announcement,
        name="admin_delete_announcement",
    ),
    path(
        "admin_view_attendance/",
        admin_views.admin_view_attendance,
        name="admin_view_attendance",
    ),
    path(
        "admin_get_attendance_dates/",
        admin_views.admin_get_attendance_dates,
        name="admin_get_attendance_dates",
    ),
    path(
        "admin_get_attendance_student/",
        admin_views.admin_get_attendance_student,
        name="admin_get_attendance_student",
    ),
    path("admin_profile/", admin_views.admin_profile, name="admin_profile"),
    path(
        "admin_profile_update/",
        admin_views.admin_profile_update,
        name="admin_profile_update",
    ),
    path("manage_leave/", admin_views.manage_leave, name="manage_leave"),
    path(
        "change_leave/<leave_id>_<status>/",
        admin_views.change_leave,
        name="change_leave",
    ),
    path(
        "admin_view_result/",
        admin_views.admin_view_result,
        name="admin_view_result",
    ),
    # URLS for Faculty
    path("faculty_home/", faculty_views.faculty_home, name="faculty_home"),
    path(
        "faculty_take_attendance/",
        faculty_views.faculty_take_attendance,
        name="faculty_take_attendance",
    ),
    path("get_students/", faculty_views.get_students, name="get_students"),
    path(
        "faculty_view_subjects/",
        faculty_views.faculty_view_subjects,
        name="faculty_view_subjects",
    ),
    path(
        "faculty_view_students/",
        faculty_views.faculty_view_students,
        name="faculty_view_students",
    ),
    path(
        "save_attendance_data/",
        faculty_views.save_attendance_data,
        name="save_attendance_data",
    ),
    path(
        "faculty_update_attendance/",
        faculty_views.faculty_update_attendance,
        name="faculty_update_attendance",
    ),
    path(
        "get_attendance_dates/",
        faculty_views.get_attendance_dates,
        name="get_attendance_dates",
    ),
    path(
        "get_attendance_student/",
        faculty_views.get_attendance_student,
        name="get_attendance_student",
    ),
    path(
        "update_attendance_data/",
        faculty_views.update_attendance_data,
        name="update_attendance_data",
    ),
    path(
        "faculty_announcement/",
        faculty_views.faculty_announcement,
        name="faculty_announcement",
    ),
    path(
        "faculty_announcement_save",
        faculty_views.faculty_announcement_save,
        name="faculty_announcement_save",
    ),
    path(
        "faculty_edit_announcement/<announcement_id>",
        faculty_views.faculty_edit_announcement,
        name="faculty_edit_announcement",
    ),
    path(
        "faculty_edit_announcement_save",
        faculty_views.faculty_edit_announcement_save,
        name="faculty_edit_announcement_save",
    ),
    path(
        "faculty_delete_announcement/<announcement_id>",
        faculty_views.faculty_delete_announcement,
        name="faculty_delete_announcement",
    ),
    path(
        "faculty_profile/",
        faculty_views.faculty_profile,
        name="faculty_profile",
    ),
    path(
        "faculty_profile_update/",
        faculty_views.faculty_profile_update,
        name="faculty_profile_update",
    ),
    path(
        "faculty_apply_leave/",
        faculty_views.faculty_apply_leave,
        name="faculty_apply_leave",
    ),
    path(
        "faculty_apply_leave_save/",
        faculty_views.faculty_apply_leave_save,
        name="faculty_apply_leave_save",
    ),
    path(
        "faculty_add_result/",
        faculty_views.faculty_add_result,
        name="faculty_add_result",
    ),
    path(
        "faculty_add_result_save/",
        faculty_views.faculty_add_result_save,
        name="faculty_add_result_save",
    ),
    # URLs for Student
    path("student_home/", student_views.student_home, name="student_home"),
    path(
        "student_view_faculty/",
        student_views.student_view_faculty,
        name="student_view_faculty",
    ),
    path(
        "student_view_subjects/",
        student_views.student_view_subjects,
        name="student_view_subjects",
    ),
    path(
        "student_view_attendance/",
        student_views.student_view_attendance,
        name="student_view_attendance",
    ),
    path(
        "student_view_attendance_post/",
        student_views.student_view_attendance_post,
        name="student_view_attendance_post",
    ),
    path(
        "student_announcement/",
        student_views.student_announcement,
        name="student_announcement",
    ),
    path(
        "student_profile/",
        student_views.student_profile,
        name="student_profile",
    ),
    path(
        "student_profile_update/",
        student_views.student_profile_update,
        name="student_profile_update",
    ),
    path(
        "student_apply_leave/",
        student_views.student_apply_leave,
        name="student_apply_leave",
    ),
    path(
        "student_apply_leave_save/",
        student_views.student_apply_leave_save,
        name="student_apply_leave_save",
    ),
    path(
        "student_view_result/",
        student_views.student_view_result,
        name="student_view_result",
    ),
    # Common views
    path(
        "delete_leave/<leave_id>/",
        common_views.delete_leave,
        name="delete_leave",
    ),
    path("feedback/", common_views.feedback, name="feedback"),
    path("feedback_save/", common_views.feedback_save, name="feedback_save"),
]
