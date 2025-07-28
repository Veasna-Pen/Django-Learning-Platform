from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.admin.sites import NotRegistered
from .models import (
    User,
    Student,
    Instructor,
    Employee,
    Category,
    Tag,
    Course,
    Enrollment,
    Lesson,
    Assignment,
    Submission,
    Review,
    LessonProgress,
)


# Custom User Admin
class CustomUserAdmin(UserAdmin):
    list_display = ("username", "email", "role", "is_staff", "is_active")
    list_filter = ("role", "is_staff", "is_active")
    fieldsets = UserAdmin.fieldsets + (("Role", {"fields": ("role",)}),)


# unregister User if it was already registered
try:
    admin.site.unregister(User)
except NotRegistered:
    pass

admin.site.register(User, CustomUserAdmin)


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ("user", "phone", "date_of_birth")
    search_fields = ("user__username", "user__email")


@admin.register(Instructor)
class InstructorAdmin(admin.ModelAdmin):
    list_display = ("user", "expertise", "years_experience")
    search_fields = ("user__username", "user__email", "expertise")


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ("user", "department", "position")
    search_fields = ("user__username", "user__email", "department")


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "description")
    search_fields = ("name",)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "instructor",
        "category",
        "price",
        "published",
        "created_date",
    )
    list_filter = ("published", "category", "created_date")
    search_fields = ("title", "instructor__user__username")
    filter_horizontal = ("tags",)


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ("student", "course", "enrolled_date", "completed", "progress")
    list_filter = ("completed", "enrolled_date")
    search_fields = ("student__user__username", "course__title")


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ("title", "course", "order", "created_date")
    list_filter = ("course", "created_date")
    search_fields = ("title", "course__title")


@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ("title", "lesson", "due_date", "max_score")
    list_filter = ("due_date", "created_date")
    search_fields = ("title", "lesson__title")


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ("student", "assignment", "submitted_date", "score", "graded")
    list_filter = ("graded", "submitted_date")
    search_fields = ("student__user__username", "assignment__title")


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("student", "course", "rating", "approved", "created_date")
    list_filter = ("rating", "approved", "created_date")
    search_fields = ("student__user__username", "course__title")


@admin.register(LessonProgress)
class LessonProgressAdmin(admin.ModelAdmin):
    list_display = ("student", "lesson", "completed", "completed_date")
    list_filter = ("completed", "completed_date")
    search_fields = ("student__user__username", "lesson__title")
