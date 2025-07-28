from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Count, Avg
from django.http import JsonResponse
from django.utils import timezone
from .models import (
    User,
    Student,
    Instructor,
    Employee,
    Course,
    Enrollment,
    Lesson,
    Assignment,
    Submission,
    Review,
    Category,
    Tag,
    LessonProgress,
)
from .forms import (
    CustomUserCreationForm,
    CourseForm,
    LessonForm,
    AssignmentForm,
    SubmissionForm,
    ReviewForm,
    GradeSubmissionForm,
)


def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Create profile based on role
            if user.role == "student":
                Student.objects.create(user=user)
            elif user.role == "instructor":
                Instructor.objects.create(user=user)
            elif user.role == "employee":
                Employee.objects.create(user=user)

            login(request, user)
            messages.success(request, "Registration successful!")
            return redirect("dashboard")
    else:
        form = CustomUserCreationForm()
    return render(request, "registration/register.html", {"form": form})


@login_required
def dashboard(request):
    user = request.user
    context = {"user": user}

    if user.role == "student":
        student = user.student_profile
        enrollments = Enrollment.objects.filter(student=student).select_related(
            "course"
        )
        upcoming_assignments = Assignment.objects.filter(
            lesson__course__enrollments__student=student, due_date__gte=timezone.now()
        ).order_by("due_date")[:5]

        context.update(
            {
                "enrollments": enrollments,
                "upcoming_assignments": upcoming_assignments,
            }
        )
        return render(request, "courses/student_dashboard.html", context)

    elif user.role == "instructor":
        instructor = user.instructor_profile
        courses = Course.objects.filter(instructor=instructor)
        total_students = Enrollment.objects.filter(
            course__instructor=instructor
        ).count()
        pending_submissions = Submission.objects.filter(
            assignment__lesson__course__instructor=instructor, graded=False
        ).count()

        context.update(
            {
                "courses": courses,
                "total_students": total_students,
                "pending_submissions": pending_submissions,
            }
        )
        return render(request, "courses/instructor_dashboard.html", context)

    elif user.role == "employee":
        total_users = User.objects.count()
        total_courses = Course.objects.count()
        total_enrollments = Enrollment.objects.count()
        recent_enrollments = Enrollment.objects.select_related(
            "student__user", "course"
        ).order_by("-enrolled_date")[:10]

        context.update(
            {
                "total_users": total_users,
                "total_courses": total_courses,
                "total_enrollments": total_enrollments,
                "recent_enrollments": recent_enrollments,
            }
        )
        return render(request, "courses/employee_dashboard.html", context)

    return render(request, "courses/dashboard.html", context)


def course_list(request):
    courses = Course.objects.filter(published=True).select_related(
        "instructor__user", "category"
    )
    categories = Category.objects.all()
    tags = Tag.objects.all()
    instructors = Instructor.objects.all()

    # Filtering
    category_filter = request.GET.get("category")
    tag_filter = request.GET.get("tag")
    instructor_filter = request.GET.get("instructor")

    if category_filter:
        courses = courses.filter(category_id=category_filter)
    if tag_filter:
        courses = courses.filter(tags__id=tag_filter)
    if instructor_filter:
        courses = courses.filter(instructor_id=instructor_filter)

    context = {
        "courses": courses,
        "categories": categories,
        "tags": tags,
        "instructors": instructors,
        "selected_category": category_filter,
        "selected_tag": tag_filter,
        "selected_instructor": instructor_filter,
    }
    return render(request, "courses/course_list.html", context)


def course_detail(request, pk):
    course = get_object_or_404(Course, pk=pk, published=True)
    lessons = course.lessons.all()
    reviews = course.reviews.filter(approved=True).select_related("student__user")

    is_enrolled = False
    enrollment = None
    if request.user.is_authenticated and request.user.role == "student":
        try:
            enrollment = Enrollment.objects.get(
                student=request.user.student_profile, course=course
            )
            is_enrolled = True
        except Enrollment.DoesNotExist:
            pass

    context = {
        "course": course,
        "lessons": lessons,
        "reviews": reviews,
        "is_enrolled": is_enrolled,
        "enrollment": enrollment,
    }
    return render(request, "courses/course_detail.html", context)


@login_required
def enroll_course(request, pk):
    if request.user.role != "student":
        messages.error(request, "Only students can enroll in courses.")
        return redirect("course_detail", pk=pk)

    course = get_object_or_404(Course, pk=pk, published=True)
    student = request.user.student_profile

    enrollment, created = Enrollment.objects.get_or_create(
        student=student, course=course
    )

    if created:
        messages.success(request, f"Successfully enrolled in {course.title}!")
    else:
        messages.info(request, f"You are already enrolled in {course.title}.")

    return redirect("course_detail", pk=pk)


@login_required
def lesson_detail(request, pk):
    lesson = get_object_or_404(Lesson, pk=pk)

    # Check if user is enrolled in the course
    if request.user.role == "student":
        try:
            enrollment = Enrollment.objects.get(
                student=request.user.student_profile, course=lesson.course
            )
        except Enrollment.DoesNotExist:
            messages.error(
                request, "You must be enrolled in this course to view lessons."
            )
            return redirect("course_detail", pk=lesson.course.pk)

        # Mark lesson as completed if not already
        progress, created = LessonProgress.objects.get_or_create(
            student=request.user.student_profile,
            lesson=lesson,
            defaults={"completed": True, "completed_date": timezone.now()},
        )
        if not progress.completed:
            progress.completed = True
            progress.completed_date = timezone.now()
            progress.save()

    assignments = lesson.assignments.all()

    context = {
        "lesson": lesson,
        "assignments": assignments,
    }
    return render(request, "courses/lesson_detail.html", context)


@login_required
def create_course(request):
    if request.user.role != "instructor":
        messages.error(request, "Only instructors can create courses.")
        return redirect("dashboard")

    if request.method == "POST":
        form = CourseForm(request.POST, request.FILES)
        if form.is_valid():
            course = form.save(commit=False)
            course.instructor = request.user.instructor_profile
            course.save()
            form.save_m2m()  # Save many-to-many relationships
            messages.success(request, "Course created successfully!")
            return redirect("course_detail", pk=course.pk)
    else:
        form = CourseForm()

    return render(request, "courses/create_course.html", {"form": form})


@login_required
def manage_courses(request):
    if request.user.role == "instructor":
        courses = Course.objects.filter(instructor=request.user.instructor_profile)
    elif request.user.role == "employee":
        courses = Course.objects.all()
    else:
        messages.error(request, "Access denied.")
        return redirect("dashboard")

    return render(request, "courses/manage_courses.html", {"courses": courses})


@login_required
def create_lesson(request, course_pk):
    course = get_object_or_404(Course, pk=course_pk)

    # Check permissions
    if (
        request.user.role == "instructor"
        and course.instructor != request.user.instructor_profile
    ):
        messages.error(request, "You can only add lessons to your own courses.")
        return redirect("course_detail", pk=course_pk)
    elif request.user.role not in ["instructor", "employee"]:
        messages.error(request, "Access denied.")
        return redirect("course_detail", pk=course_pk)

    if request.method == "POST":
        form = LessonForm(request.POST, request.FILES)
        if form.is_valid():
            lesson = form.save(commit=False)
            lesson.course = course
            lesson.save()
            messages.success(request, "Lesson created successfully!")
            return redirect("course_detail", pk=course_pk)
    else:
        form = LessonForm()

    return render(
        request, "courses/create_lesson.html", {"form": form, "course": course}
    )


@login_required
def create_assignment(request, lesson_pk):
    lesson = get_object_or_404(Lesson, pk=lesson_pk)

    # Check permissions
    if (
        request.user.role == "instructor"
        and lesson.course.instructor != request.user.instructor_profile
    ):
        messages.error(request, "You can only add assignments to your own lessons.")
        return redirect("lesson_detail", pk=lesson_pk)
    elif request.user.role not in ["instructor", "employee"]:
        messages.error(request, "Access denied.")
        return redirect("lesson_detail", pk=lesson_pk)

    if request.method == "POST":
        form = AssignmentForm(request.POST)
        if form.is_valid():
            assignment = form.save(commit=False)
            assignment.lesson = lesson
            assignment.save()
            messages.success(request, "Assignment created successfully!")
            return redirect("lesson_detail", pk=lesson_pk)
    else:
        form = AssignmentForm()

    return render(
        request, "courses/create_assignment.html", {"form": form, "lesson": lesson}
    )


@login_required
def assignment_detail(request, pk):
    assignment = get_object_or_404(Assignment, pk=pk)

    submission = None
    if request.user.role == "student":
        try:
            submission = Submission.objects.get(
                assignment=assignment, student=request.user.student_profile
            )
        except Submission.DoesNotExist:
            pass

    context = {
        "assignment": assignment,
        "submission": submission,
    }
    return render(request, "courses/assignment_detail.html", context)


@login_required
def submit_assignment(request, pk):
    assignment = get_object_or_404(Assignment, pk=pk)

    if request.user.role != "student":
        messages.error(request, "Only students can submit assignments.")
        return redirect("assignment_detail", pk=pk)

    # Check if already submitted
    try:
        submission = Submission.objects.get(
            assignment=assignment, student=request.user.student_profile
        )
        messages.info(request, "You have already submitted this assignment.")
        return redirect("assignment_detail", pk=pk)
    except Submission.DoesNotExist:
        pass

    if request.method == "POST":
        form = SubmissionForm(request.POST, request.FILES)
        if form.is_valid():
            submission = form.save(commit=False)
            submission.assignment = assignment
            submission.student = request.user.student_profile
            submission.save()
            messages.success(request, "Assignment submitted successfully!")
            return redirect("assignment_detail", pk=pk)
    else:
        form = SubmissionForm()

    return render(
        request,
        "courses/submit_assignment.html",
        {"form": form, "assignment": assignment},
    )


@login_required
def grade_submissions(request):
    if request.user.role != "instructor":
        messages.error(request, "Only instructors can grade submissions.")
        return redirect("dashboard")

    submissions = Submission.objects.filter(
        assignment__lesson__course__instructor=request.user.instructor_profile,
        graded=False,
    ).select_related("student__user", "assignment__lesson__course")

    return render(
        request, "courses/grade_submissions.html", {"submissions": submissions}
    )


@login_required
def grade_submission(request, pk):
    submission = get_object_or_404(Submission, pk=pk)

    if (
        request.user.role != "instructor"
        or submission.assignment.lesson.course.instructor
        != request.user.instructor_profile
    ):
        messages.error(request, "Access denied.")
        return redirect("dashboard")

    if request.method == "POST":
        form = GradeSubmissionForm(request.POST, instance=submission)
        if form.is_valid():
            submission = form.save(commit=False)
            submission.graded = True
            submission.save()
            messages.success(request, "Submission graded successfully!")
            return redirect("grade_submissions")
    else:
        form = GradeSubmissionForm(instance=submission)

    return render(
        request,
        "courses/grade_submission.html",
        {"form": form, "submission": submission},
    )


@login_required
def create_review(request, course_pk):
    course = get_object_or_404(Course, pk=course_pk)

    if request.user.role != "student":
        messages.error(request, "Only students can write reviews.")
        return redirect("course_detail", pk=course_pk)

    # Check if student is enrolled
    try:
        Enrollment.objects.get(student=request.user.student_profile, course=course)
    except Enrollment.DoesNotExist:
        messages.error(
            request, "You must be enrolled in this course to write a review."
        )
        return redirect("course_detail", pk=course_pk)

    # Check if already reviewed
    if Review.objects.filter(
        course=course, student=request.user.student_profile
    ).exists():
        messages.info(request, "You have already reviewed this course.")
        return redirect("course_detail", pk=course_pk)

    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.course = course
            review.student = request.user.student_profile
            review.save()
            messages.success(request, "Review submitted successfully!")
            return redirect("course_detail", pk=course_pk)
    else:
        form = ReviewForm()

    return render(
        request, "courses/create_review.html", {"form": form, "course": course}
    )


@login_required
def my_grades(request):
    if request.user.role != "student":
        messages.error(request, "Only students can view grades.")
        return redirect("dashboard")

    submissions = Submission.objects.filter(
        student=request.user.student_profile, graded=True
    ).select_related("assignment__lesson__course")

    return render(request, "courses/my_grades.html", {"submissions": submissions})
