EduLearn: Technical Platform Description

This document outlines the technical architecture, components, and implementation strategy for the EduLearn e-learning platform.

 **1. Core Technology Stack**

The platform will be built as a monolithic web application using a robust and rapid development stack:

  * **Backend Framework:** **Django 4.x** (using Python 3.10+)
  * **Database:**
      * **Development:** **SQLite** (for simplicity and zero-configuration setup).
      * **Production:** **PostgreSQL** (for scalability, data integrity, and performance).
  * **Frontend Styling:** **Tailwind CSS 3.x** (for a utility-first, custom design approach).
  * **Frontend Interactivity:** Minimal JavaScript, using **Alpine.js** for small, component-level interactions (e.g., dropdowns, tabs) to avoid the overhead of a large JS framework.
  * **Application Server (Production):** **Gunicorn**
  * **Web Server (Production):** **Nginx** (to serve static/media files and act as a reverse proxy).

-----

 **2. Project Structure**

The project will be organized into a core project directory and several dedicated Django "apps," each responsible for a distinct domain of functionality.

```
edulearn_project/
├── edulearn/         # Core project settings, urls.py, wsgi.py
├── courses/          # App for courses, lessons, resources
├── users/            # App for user profiles, roles, authentication
├── quizzes/          # App for quizzes, questions, and attempts
├── dashboard/        # App for the personalized learner dashboard
├── static/           # For compiled CSS, JS, and project-wide images
├── templates/        # For base templates (base.html, nav.html, etc.)
└── manage.py
```

-----

**3. Data Models (`models.py`)**

The database schema is the backbone of the application, defined via Django's Object-Relational Mapper (ORM).

**`users.models.py`**

  * **`UserProfile`**: A one-to-one extension of Django's built-in `User` model.
      * `user`: `OneToOneField` to `django.contrib.auth.models.User`.
      * `role`: `CharField` with choices (`'learner'`, `'instructor'`, `'admin'`).
      * `bio`: `TextField` (optional).
      * `avatar`: `ImageField`.

**`courses.models.py`**

  * **`Category`**: For organizing courses.
      * `name`: `CharField`.
      * `slug`: `SlugField` (for clean URLs).
  * **`Course`**: The main course model.
      * `category`: `ForeignKey` to `Category`.
      * `instructor`: `ForeignKey` to `User`.
      * `title`: `CharField`.
      * `description`: `TextField`.
      * `thumbnail`: `ImageField`.
      * `created_at`: `DateTimeField` (auto-populated).
  * **`Enrollment`**: A through-model linking users to courses.
      * `student`: `ForeignKey` to `User`.
      * `course`: `ForeignKey` to `Course`.
      * `enrolled_at`: `DateTimeField` (auto-populated).
  * **`Lesson`**: Individual lessons within a course.
      * `course`: `ForeignKey` to `Course`.
      * `title`: `CharField`.
      * `lesson_number`: `PositiveIntegerField`.
      * `video_file`: `FileField` (for video uploads).
      * `content`: `TextField` (for text-based content).
  * **`Resource`**: Downloadable materials for a lesson.
      * `lesson`: `ForeignKey` to `Lesson`.
      * `title`: `CharField`.
      * `file`: `FileField`.

**`quizzes.models.py`**

  * **`Quiz`**: A quiz associated with a course.
      * `course`: `ForeignKey` to `Course`.
      * `title`: `CharField`.
  * **`Question`**: A question within a quiz.
      * `quiz`: `ForeignKey` to `Quiz`.
      * `text`: `TextField`.
  * **`Choice`**: A multiple-choice answer for a question.
      * `question`: `ForeignKey` to `Question`.
      * `text`: `CharField`.
      * `is_correct`: `BooleanField`.
  * **`QuizAttempt`**: Records a user's attempt at a quiz.
      * `student`: `ForeignKey` to `User`.
      * `quiz`: `ForeignKey` to `Quiz`.
      * `score`: `FloatField`.
      * `completed_at`: `DateTimeField` (auto-populated).

-----

 **4. Core Functionality (`views.py` & `urls.py`)**

  * **Authentication Flow:**
      * Will leverage Django's built-in `django.contrib.auth.views` for login, logout, and password reset functionality.
      * A custom view will handle user registration, creating both a `User` and a `UserProfile` instance.
  * **Course Catalog & Enrollment:**
      * A `CourseListView` will display all published courses, with filtering by `Category`.
      * A `CourseDetailView` will show a single course's page, including its lesson list. The view logic will check if `request.user` has an `Enrollment` record for the course to display an "Enroll" or "Go to Course" button.
  * **Lesson & Content Access:**
      * A `LessonDetailView` will display lesson content. It will use a permission mixin (e.g., `UserPassesTestMixin`) to ensure only enrolled students can view the page.
  * **Quiz Taking & Scoring:**
      * A `QuizDetailView` will display the quiz questions and choices using a Django `FormSet`.
      * On POST request, the view will process the submitted `FormSet`, compare answers to the `is_correct` flag on the `Choice` model, calculate a percentage score, and save it as a new `QuizAttempt` record before redirecting to a results page.
  * **Learner Dashboard:**
      * A `DashboardView` will be the main entry point after login.
      * It will aggregate data specific to the logged-in user:
          * `Enrollment.objects.filter(student=request.user)` to get "My Courses".
          * `QuizAttempt.objects.filter(student=request.user)` to calculate average score and show quiz history.
          * Calculate "Time Spent Learning" (this would require adding a progress tracking model, e.g., `LessonCompletion`).

-----

 **5. Frontend Implementation**

  * **Templating:**
      * A `base.html` template will define the main site structure, including the header, footer, and links to the compiled CSS file.
      * All other templates (`course_catalog.html`, `lesson_detail.html`, etc.) will use `{% extends 'base.html' %}` to maintain a consistent layout.
      * Navigation bars and other reusable components will be organized into `{% include %}`-able snippets.
  * **Styling (Tailwind CSS):**
      * The `npm run build:css` command (configured in `package.json`) will be used during development to watch for changes in template files and re-compile the `static/css/output.css` file.
      * All styling will be applied directly in the HTML templates using Tailwind's utility classes (e.g., `<div class="p-6 bg-white rounded-lg shadow-md">`).
  * **Admin Panel:**
      * The built-in `django.contrib.admin` will serve as the complete backend for Instructors and Administrators.
      * Models will be registered in each app's `admin.py`. `list_display`, `list_filter`, and `search_fields` will be configured to create a user-friendly management interface for courses, users, and quizzes. This completely eliminates the need to build a separate admin frontend.
