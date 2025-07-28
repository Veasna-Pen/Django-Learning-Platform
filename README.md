# Django Learning Platform

---

## Features

### User Management

- **Three User Roles**: Student, Instructor, Employee
- **Custom User Model** with role-based authentication and permissions
- **Role-specific Dashboards** tailored to each user type
- **Profile Management** with role-specific information

### Course Management

- **Course Creation & Editing** by instructors, with rich text descriptions
- **Category and Tag System** for effective course organization and discovery
- **Advanced Course Filtering** by category, tag, and instructor
- **Course Publishing Workflow** for controlled content release
- **Multimedia Support** for course images and banners

### Learning Content

- **Lesson Management** supporting videos, PDFs, and other documents
- **External Video Embedding** (YouTube, Vimeo, etc.)
- **Secure File Uploads** for lesson materials
- **Custom Lesson Ordering** with student progress tracking

### Enrollment System

- **Student Enrollment** with self-service and administrative options
- **Real-Time Progress Tracking** per course and lesson
- **Lesson Completion Tracking** with visual indicators
- **Enrollment Management** by employees for oversight

### Assignment System

- **Assignment Creation** by instructors linked to lessons
- **Flexible Submission Types** including file uploads and text input
- **Grading Interface** with scores, comments, and feedback
- **Due Date Enforcement** and deadline management
- **Grade History & Tracking** accessible to students and instructors

### Review System

- **Course Reviews & Ratings** from enrolled students
- **5-Star Rating System** with textual feedback
- **Review Moderation** by employees for quality control
- **Aggregate Rating Calculation** for course summaries

### Administration

- **Full Django Admin Integration** for all models
- **Employee Dashboard** with site-wide statistics and controls
- **Comprehensive Course & User Management Tools**

---

## Installation

1. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

2. **Run migrations**

   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

3. **Load sample data**

   ```bash
   python scripts/create_sample_data.py
   ```

4. **Create superuser (optional)**

   ```bash
   python manage.py createsuperuser
   ```

5. **Start the development server**

   ```bash
   python manage.py runserver
   ```

6. **Access the application**
   - Main site: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
   - Admin panel: [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

---

## Demo Credentials

| Role       | Username     | Password      | Capabilities                                                        |
| ---------- | ------------ | ------------- | ------------------------------------------------------------------- |
| Student    | `student`    | `testpass123` | Enroll in courses, view lessons, submit assignments, leave reviews  |
| Instructor | `instructor` | `testpass123` | Create courses, manage lessons & assignments, grade submissions     |
| Employee   | `employee`   | `testpass123` | Manage system settings, oversee courses & users, access admin panel |

---

## Project Structure

learning_platform/
├── learning_platform/ # Django project settings
├── courses/ # Main app containing core functionality
│ ├── models.py # Database models
│ ├── views.py # Views and business logic
│ ├── forms.py # Forms for user input
│ ├── admin.py # Admin site configurations
│ └── urls.py # URL routing
├── templates/ # HTML templates
│ ├── base.html # Base layout template
│ ├── registration/ # Authentication-related templates
│ └── courses/ # Course and lesson templates
├── static/ # Static files (CSS, JS, images)
├── media/ # User-uploaded files
├── scripts/ # Utility scripts (e.g., sample data loaders)
└── requirements.txt # Python package dependencies

---

## Models Overview

### User Management

- **User**: Custom user model with role field (Student, Instructor, Employee)
- **StudentProfile**: Extended info for students
- **InstructorProfile**: Expertise and bio for instructors
- **EmployeeProfile**: Department and admin info for employees

### Course System

- **Category**: Course categories (one-to-many)
- **Tag**: Tags for flexible course labeling (many-to-many)
- **Course**: Core course entity with metadata and content
- **Enrollment**: Tracks student registrations and statuses

### Learning Content

- **Lesson**: Individual lesson units within courses
- **LessonProgress**: Student-specific progress tracker

### Assignment System

- **Assignment**: Linked to lessons with deadlines
- **Submission**: Student assignment submissions with grading data

### Review System

- **Review**: Course reviews and ratings submitted by students

---

## Key Implementation Details

### Role-Based Access Control

- Custom decorators and view-level permissions enforce role restrictions
- Dynamic dashboards and navigation based on user roles
- Template logic controls content visibility by role

### File Upload Handling

- Secure handling of course images, lesson videos, PDFs, and assignment files
- Organized media directories per content type
- Development-time media serving with Django settings

### Progress Tracking

- Automatic marking of lesson completion
- Calculation of course progress percentages
- Visual progress indicators on student dashboards

### Filtering and Search

- Multi-criteria course filtering (category, tags, instructor)
- Clean URLs to preserve filter state
- Responsive UI with filtering controls

### Grading System

- Instructor-friendly grading interface with inline feedback
- Score calculation and grade summaries
- Student grade display with instructor comments

---

## Security Features

- CSRF protection on all forms by default
- Role-based authentication and authorization checks
- Validation and sanitization of file uploads
- Use of Django ORM to prevent SQL injection
- Secure password storage with Django's built-in hashing

---

## Responsive Design

- Built with Bootstrap 5 for mobile-first responsiveness
- Intuitive mobile navigation and menus
- Responsive tables, cards, and forms
- Touch-friendly interactive elements

---

## Future Enhancements

- Real-time notifications and alerts
- Discussion forums and Q&A boards
- Integrated video streaming and hosting
- Payment gateway integration for paid courses
- Certificate generation upon course completion
- Advanced analytics and reporting dashboards
- Support for live, interactive video classes

---
