# Generated by Django 3.0.7 on 2021-11-22 06:14

import django.contrib.auth.models
import django.contrib.auth.validators
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("auth", "0011_update_proxy_permissions"),
    ]

    operations = [
        migrations.CreateModel(
            name="BaseUser",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "password",
                    models.CharField(max_length=128, verbose_name="password"),
                ),
                (
                    "last_login",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="last login"
                    ),
                ),
                (
                    "is_superuser",
                    models.BooleanField(
                        default=False,
                        help_text="Designates that this user has all permissions without explicitly assigning them.",
                        verbose_name="superuser status",
                    ),
                ),
                (
                    "username",
                    models.CharField(
                        error_messages={
                            "unique": "A user with that username already exists."
                        },
                        help_text="Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.",
                        max_length=150,
                        unique=True,
                        validators=[
                            django.contrib.auth.validators.UnicodeUsernameValidator()
                        ],
                        verbose_name="username",
                    ),
                ),
                (
                    "first_name",
                    models.CharField(
                        blank=True, max_length=30, verbose_name="first name"
                    ),
                ),
                (
                    "last_name",
                    models.CharField(
                        blank=True, max_length=150, verbose_name="last name"
                    ),
                ),
                (
                    "email",
                    models.EmailField(
                        blank=True,
                        max_length=254,
                        verbose_name="email address",
                    ),
                ),
                (
                    "is_staff",
                    models.BooleanField(
                        default=False,
                        help_text="Designates whether the user can log into this admin site.",
                        verbose_name="staff status",
                    ),
                ),
                (
                    "is_active",
                    models.BooleanField(
                        default=True,
                        help_text="Designates whether this user should be treated as active. Unselect this instead of deleting accounts.",
                        verbose_name="active",
                    ),
                ),
                (
                    "date_joined",
                    models.DateTimeField(
                        default=django.utils.timezone.now,
                        verbose_name="date joined",
                    ),
                ),
                (
                    "user_type",
                    models.CharField(
                        choices=[(1, "Admin"), (2, "Faculty"), (3, "Student")],
                        default=1,
                        max_length=10,
                    ),
                ),
                (
                    "groups",
                    models.ManyToManyField(
                        blank=True,
                        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.Group",
                        verbose_name="groups",
                    ),
                ),
                (
                    "user_permissions",
                    models.ManyToManyField(
                        blank=True,
                        help_text="Specific permissions for this user.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.Permission",
                        verbose_name="user permissions",
                    ),
                ),
            ],
            options={
                "verbose_name": "user",
                "verbose_name_plural": "users",
                "abstract": False,
            },
            managers=[("objects", django.contrib.auth.models.UserManager()),],
        ),
        migrations.CreateModel(
            name="Attendance",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("attendance_date", models.DateField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name="Course",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("course_name", models.CharField(max_length=255)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name="Faculty",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("address", models.TextField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "admin",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Semester",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("start_year", models.DateField()),
                ("end_year", models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name="Subject",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("subject_name", models.CharField(max_length=255)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "course_id",
                    models.ForeignKey(
                        default=1,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="university_connect.Course",
                    ),
                ),
                (
                    "faculty_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Student",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("gender", models.CharField(max_length=50)),
                ("profile_pic", models.FileField(upload_to="")),
                ("address", models.TextField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "admin",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "course_id",
                    models.ForeignKey(
                        default=1,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to="university_connect.Course",
                    ),
                ),
                (
                    "semester_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="university_connect.Semester",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="FeedbackStudent",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("feedback", models.TextField()),
                ("feedback_reply", models.TextField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "student_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="university_connect.Student",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="FeedbackFaculty",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("feedback", models.TextField()),
                ("feedback_reply", models.TextField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "faculty_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="university_connect.Faculty",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="AttendanceReport",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("status", models.BooleanField(default=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "attendance_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="university_connect.Attendance",
                    ),
                ),
                (
                    "student_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to="university_connect.Student",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="attendance",
            name="semester_id",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="university_connect.Semester",
            ),
        ),
        migrations.AddField(
            model_name="attendance",
            name="subject_id",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.DO_NOTHING,
                to="university_connect.Subject",
            ),
        ),
        migrations.CreateModel(
            name="Announcement",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("message", models.TextField(blank=True)),
                ("link", models.URLField(blank=True)),
                (
                    "upload_url",
                    models.FileField(
                        blank=True,
                        upload_to="assignments/<django.db.models.fields.related.ForeignKey>",
                    ),
                ),
                ("upload_name", models.TextField(blank=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "faculty_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="university_connect.Faculty",
                    ),
                ),
                (
                    "subject_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="university_connect.Subject",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Admin",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "admin",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
