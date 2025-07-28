from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Authentication
    path('', views.course_list, name='home'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),
    
    # Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # Courses
    path('courses/', views.course_list, name='course_list'),
    path('courses/<int:pk>/', views.course_detail, name='course_detail'),
    path('courses/<int:pk>/enroll/', views.enroll_course, name='enroll_course'),
    path('courses/create/', views.create_course, name='create_course'),
    path('courses/manage/', views.manage_courses, name='manage_courses'),
    
    # Lessons
    path('lessons/<int:pk>/', views.lesson_detail, name='lesson_detail'),
    path('courses/<int:course_pk>/lessons/create/', views.create_lesson, name='create_lesson'),
    
    # Assignments
    path('assignments/<int:pk>/', views.assignment_detail, name='assignment_detail'),
    path('assignments/<int:pk>/submit/', views.submit_assignment, name='submit_assignment'),
    path('lessons/<int:lesson_pk>/assignments/create/', views.create_assignment, name='create_assignment'),
    path('submissions/grade/', views.grade_submissions, name='grade_submissions'),
    path('submissions/<int:pk>/grade/', views.grade_submission, name='grade_submission'),
    path('grades/', views.my_grades, name='my_grades'),
    
    # Reviews
    path('courses/<int:course_pk>/review/', views.create_review, name='create_review'),
]
