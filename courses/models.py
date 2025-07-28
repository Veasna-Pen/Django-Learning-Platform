from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.core.validators import MinValueValidator, MaxValueValidator


class User(AbstractUser):
    ROLE_CHOICES = [
        ("student", "Student"),
        ("instructor", "Instructor"),
        ("employee", "Employee"),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="student")

    def get_profile(self):
        if self.role == "student":
            return getattr(self, "student_profile", None)
        elif self.role == "instructor":
            return getattr(self, "instructor_profile", None)
        elif self.role == "employee":
            return getattr(self, "employee_profile", None)
        return None


class Student(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="student_profile"
    )
    date_of_birth = models.DateField(null=True, blank=True)
    phone = models.CharField(max_length=15, blank=True)
    bio = models.TextField(blank=True)

    def __str__(self):
        return f"Student: {self.user.username}"


class Instructor(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="instructor_profile"
    )
    bio = models.TextField(blank=True)
    expertise = models.CharField(max_length=200, blank=True)
    years_experience = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Instructor: {self.user.username}"


class Employee(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="employee_profile"
    )
    department = models.CharField(max_length=100, blank=True)
    position = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"Employee: {self.user.username}"


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Course(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    instructor = models.ForeignKey(
        Instructor, on_delete=models.CASCADE, related_name="courses"
    )
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="courses"
    )
    tags = models.ManyToManyField(Tag, blank=True, related_name="courses")
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    image = models.ImageField(upload_to="course_images/", blank=True, null=True)
    published = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_date"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("course_detail", kwargs={"pk": self.pk})

    @property
    def average_rating(self):
        reviews = self.reviews.all()
        if reviews:
            return sum([review.rating for review in reviews]) / len(reviews)
        return 0

    @property
    def total_lessons(self):
        return self.lessons.count()


class Enrollment(models.Model):
    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, related_name="enrollments"
    )
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name="enrollments"
    )
    enrolled_date = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)
    progress = models.PositiveIntegerField(
        default=0, validators=[MaxValueValidator(100)]
    )

    class Meta:
        unique_together = ["student", "course"]

    def __str__(self):
        return f"{self.student.user.username} enrolled in {self.course.title}"


class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="lessons")
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    video_url = models.URLField(
        blank=True, help_text="External video link (YouTube, Vimeo, etc.)"
    )
    video_file = models.FileField(upload_to="lesson_videos/", blank=True, null=True)
    pdf_file = models.FileField(upload_to="lesson_pdfs/", blank=True, null=True)
    order = models.PositiveIntegerField(default=0)
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["order", "created_date"]

    def __str__(self):
        return f"{self.course.title} - {self.title}"


class Assignment(models.Model):
    lesson = models.ForeignKey(
        Lesson, on_delete=models.CASCADE, related_name="assignments"
    )
    title = models.CharField(max_length=200)
    description = models.TextField()
    due_date = models.DateTimeField()
    max_score = models.PositiveIntegerField(default=100)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.lesson.title} - {self.title}"


class Submission(models.Model):
    assignment = models.ForeignKey(
        Assignment, on_delete=models.CASCADE, related_name="submissions"
    )
    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, related_name="submissions"
    )
    content = models.TextField(blank=True, help_text="Text/code submission")
    file = models.FileField(upload_to="submissions/", blank=True, null=True)
    submitted_date = models.DateTimeField(auto_now_add=True)
    score = models.PositiveIntegerField(
        null=True, blank=True, validators=[MaxValueValidator(100)]
    )
    feedback = models.TextField(blank=True)
    graded = models.BooleanField(default=False)

    class Meta:
        unique_together = ["assignment", "student"]

    def __str__(self):
        return f"{self.student.user.username} - {self.assignment.title}"


class Review(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="reviews")
    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, related_name="reviews"
    )
    rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    comment = models.TextField(blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=True)

    class Meta:
        unique_together = ["course", "student"]

    def __str__(self):
        return f"{self.student.user.username} - {self.course.title} ({self.rating}/5)"


class LessonProgress(models.Model):
    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, related_name="lesson_progress"
    )
    lesson = models.ForeignKey(
        Lesson, on_delete=models.CASCADE, related_name="progress"
    )
    completed = models.BooleanField(default=False)
    completed_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ["student", "lesson"]

    def __str__(self):
        return f"{self.student.user.username} - {self.lesson.title}"
