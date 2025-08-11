from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from courses.models import Enrollment
from quizzes.models import QuizAttempt
from django.db.models import Avg

@login_required
def dashboard_view(request):
    enrolled_courses = Enrollment.objects.filter(student=request.user)
    quiz_attempts = QuizAttempt.objects.filter(student=request.user)

    average_score = quiz_attempts.aggregate(Avg('score'))['score__avg']

    context = {
        'enrolled_courses': enrolled_courses,
        'quiz_attempts': quiz_attempts,
        'average_score': average_score,
    }
    return render(request, 'dashboard/dashboard.html', context)
