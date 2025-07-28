import os
import sys
import django

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "learning_platform.settings")
django.setup()

from django.contrib.auth import get_user_model
from courses.models import *
from django.utils import timezone
from datetime import timedelta

User = get_user_model()


def create_sample_data():
    print("Creating sample data...")

    # Create demo users
    student_user, created = User.objects.get_or_create(
        username="student",
        defaults={
            "email": "student@example.com",
            "role": "student",
            "first_name": "John",
            "last_name": "Student",
        },
    )
    if created:
        student_user.set_password("testpass123")
        student_user.save()
        Student.objects.create(
            user=student_user,
            bio="I'm a passionate learner interested in technology and programming.",
        )

    instructor_user, created = User.objects.get_or_create(
        username="instructor",
        defaults={
            "email": "instructor@example.com",
            "role": "instructor",
            "first_name": "Jane",
            "last_name": "Teacher",
        },
    )
    if created:
        instructor_user.set_password("testpass123")
        instructor_user.save()
        Instructor.objects.create(
            user=instructor_user,
            bio="Experienced software developer and educator with 10+ years in the industry.",
            expertise="Web Development, Python, JavaScript",
            years_experience=10,
        )

    employee_user, created = User.objects.get_or_create(
        username="employee",
        defaults={
            "email": "employee@example.com",
            "role": "employee",
            "first_name": "Admin",
            "last_name": "User",
        },
    )
    if created:
        employee_user.set_password("testpass123")
        employee_user.save()
        Employee.objects.create(
            user=employee_user, department="IT", position="System Administrator"
        )

    # Create categories
    categories_data = [
        {
            "name": "Programming",
            "description": "Learn various programming languages and concepts",
        },
        {
            "name": "Web Development",
            "description": "Frontend and backend web development",
        },
        {
            "name": "Data Science",
            "description": "Data analysis, machine learning, and statistics",
        },
        {"name": "Design", "description": "UI/UX design and graphic design"},
        {"name": "Business", "description": "Business skills and entrepreneurship"},
    ]

    for cat_data in categories_data:
        Category.objects.get_or_create(name=cat_data["name"], defaults=cat_data)

    # Create tags
    tags_data = [
        "Python",
        "JavaScript",
        "HTML",
        "CSS",
        "React",
        "Django",
        "Machine Learning",
        "AI",
        "Database",
        "API",
    ]
    for tag_name in tags_data:
        Tag.objects.get_or_create(name=tag_name)

    # Create sample courses
    instructor = Instructor.objects.get(user__username="instructor")
    programming_category = Category.objects.get(name="Programming")
    web_dev_category = Category.objects.get(name="Web Development")

    # Course 1: Python for Beginners
    python_course, created = Course.objects.get_or_create(
        title="Python Programming for Beginners",
        defaults={
            "description": """Learn Python programming from scratch! This comprehensive course covers all the fundamentals you need to start your programming journey.

            What you'll learn:
            - Python syntax and basic concepts
            - Data types and variables
            - Control structures (if/else, loops)
            - Functions and modules
            - Object-oriented programming
            - File handling and error management
            - Working with libraries and APIs

            Perfect for complete beginners with no prior programming experience!""",
            "instructor": instructor,
            "category": programming_category,
            "price": 49.99,
            "published": True,
        },
    )

    if created:
        python_tags = Tag.objects.filter(name__in=["Python", "Programming"])
        python_course.tags.set(python_tags)

    # Course 2: Web Development with Django
    django_course, created = Course.objects.get_or_create(
        title="Web Development with Django",
        defaults={
            "description": """Build powerful web applications using Django, the high-level Python web framework.

            Course content:
            - Django fundamentals and MVC architecture
            - Models, Views, and Templates
            - URL routing and forms
            - User authentication and authorization
            - Database integration with ORM
            - RESTful APIs with Django REST Framework
            - Deployment and production considerations

            Prerequisites: Basic Python knowledge recommended.""",
            "instructor": instructor,
            "category": web_dev_category,
            "price": 79.99,
            "published": True,
        },
    )

    if created:
        django_tags = Tag.objects.filter(
            name__in=["Python", "Django", "Web Development"]
        )
        django_course.tags.set(django_tags)

    # Create lessons for Python course
    if created or not python_course.lessons.exists():
        lessons_data = [
            {
                "title": "Introduction to Python",
                "description": "Overview of Python programming language and setting up the development environment.",
                "order": 1,
                "video_url": "https://www.youtube.com/embed/kqtD5dpn9C8",
            },
            {
                "title": "Variables and Data Types",
                "description": "Learn about different data types in Python and how to work with variables.",
                "order": 2,
                "video_url": "https://www.youtube.com/embed/OH86oLzVzzw",
            },
            {
                "title": "Control Structures",
                "description": "Understanding if/else statements, loops, and conditional logic.",
                "order": 3,
                "video_url": "https://www.youtube.com/embed/DZwmZ8Usvnk",
            },
            {
                "title": "Functions and Modules",
                "description": "Creating reusable code with functions and organizing code with modules.",
                "order": 4,
                "video_url": "https://www.youtube.com/embed/9Os0o3wzS_I",
            },
        ]

        for lesson_data in lessons_data:
            Lesson.objects.get_or_create(
                course=python_course, title=lesson_data["title"], defaults=lesson_data
            )

    # Create sample enrollment
    student = Student.objects.get(user__username="student")
    enrollment, created = Enrollment.objects.get_or_create(
        student=student, course=python_course, defaults={"progress": 25}
    )

    # Create sample assignment
    first_lesson = python_course.lessons.first()
    if first_lesson:
        assignment, created = Assignment.objects.get_or_create(
            lesson=first_lesson,
            title="Python Basics Quiz",
            defaults={
                "description": """Complete this assignment to test your understanding of Python basics.

                Tasks:
                1. Write a Python program that asks for the user's name and age
                2. Calculate and display the year they were born
                3. Use proper variable names and comments
                4. Handle potential errors (bonus points)

                Submit your code as a .py file or paste it in the text area below.""",
                "due_date": timezone.now() + timedelta(days=7),
                "max_score": 100,
            },
        )

    # Create sample review
    review, created = Review.objects.get_or_create(
        course=python_course,
        student=student,
        defaults={
            "rating": 5,
            "comment": "Excellent course! The instructor explains concepts clearly and the hands-on exercises are very helpful. Highly recommended for beginners.",
        },
    )

    print("Sample data created successfully!")
    print("\nDemo login credentials:")
    print("Student - Username: student, Password: testpass123")
    print("Instructor - Username: instructor, Password: testpass123")
    print("Employee - Username: employee, Password: testpass123")


if __name__ == "__main__":
    create_sample_data()
