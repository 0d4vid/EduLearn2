# EduLearn E-Learning Platform

Welcome to EduLearn, a modern e-learning platform built with Django. This project is an MVP (Minimum Viable Product) that provides the core functionalities for an online learning environment.

See the `TECHNICAL_DESCRIPTION.md` file for the detailed technical specification that was used to build this project.

## Features

*   **User Authentication:** Secure user registration, login, and logout.
*   **Course Catalog:** Browse a list of available courses.
*   **Course Enrollment:** Users can enroll in courses to gain access to content.
*   **Lesson Viewing:** Enrolled students can view course lessons, which can include text and video content.
*   **Quizzes:** Test your knowledge with quizzes associated with each course. Your attempts and scores are saved.
*   **Personalized Dashboard:** A dashboard for each user to track their enrolled courses and quiz progress.
*   **Admin Panel:** A complete backend interface for administrators and instructors to manage courses, users, and quizzes.

## Tech Stack

*   **Backend:** Django 4.x
*   **Database:** SQLite (for development)
*   **Frontend:** Tailwind CSS (via Play CDN)

## Setup and Installation

To run this project locally, follow these steps:

1.  **Clone the repository:**
    ```bash
    git clone <repository_url>
    cd edulearn_project
    ```

2.  **Create a virtual environment and install dependencies:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    pip install -r requirements.txt
    ```
    *(Note: A `requirements.txt` file would need to be generated via `pip freeze > requirements.txt`)*

3.  **Apply database migrations:**
    ```bash
    python manage.py migrate
    ```

4.  **Create a superuser to access the admin panel:**
    ```bash
    python manage.py createsuperuser
    ```

5.  **Run the development server:**
    ```bash
    python manage.py runserver
    ```

The application will be available at `http://127.0.0.1:8000/`. The admin panel is at `http://127.0.0.1:8000/admin/`.
