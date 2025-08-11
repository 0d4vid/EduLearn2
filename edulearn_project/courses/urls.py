from django.urls import path
from .views import CourseListView, CourseDetailView, EnrollView, LessonDetailView

app_name = 'courses'

urlpatterns = [
    path('', CourseListView.as_view(), name='course_list'),
    path('<int:pk>/', CourseDetailView.as_view(), name='course_detail'),
    path('<int:course_id>/enroll/', EnrollView.as_view(), name='enroll'),
    path('lessons/<int:pk>/', LessonDetailView.as_view(), name='lesson_detail'),
]
