from django.urls import path
from .views import quiz_view

app_name = 'quizzes'

urlpatterns = [
    path('<int:quiz_id>/', quiz_view, name='quiz_detail'),
]
