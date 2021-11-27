from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import (
    Admin,
    Announcement,
    Attendance,
    AttendanceReport,
    BaseUser,
    Course,
    Faculty,
    Feedback,
    Student,
    Subject,
)


# Register your models here.
class UserModel(UserAdmin):
    pass


admin.site.register(BaseUser, UserModel)

admin.site.register(Admin)
admin.site.register(Faculty)
admin.site.register(Course)
admin.site.register(Subject)
admin.site.register(Student)
admin.site.register(Attendance)
admin.site.register(AttendanceReport)
admin.site.register(Feedback)
admin.site.register(Announcement)
