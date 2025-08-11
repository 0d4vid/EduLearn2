from django.shortcuts import render, redirect, get_object_or_404
from .models import Quiz, Question, Choice, QuizAttempt
from django.contrib.auth.decorators import login_required

@login_required
def quiz_view(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    questions = quiz.questions.all()

    if request.method == 'POST':
        score = 0
        total = 0
        for question in questions:
            choice_id = request.POST.get(f'question_{question.id}')
            if choice_id:
                choice = Choice.objects.get(id=choice_id)
                if choice.is_correct:
                    score += 1
            total += 1

        percentage_score = (score / total) * 100 if total > 0 else 0

        QuizAttempt.objects.create(
            student=request.user,
            quiz=quiz,
            score=percentage_score
        )
        # Redirect to a results page (to be created)
        return redirect('dashboard:home')

    return render(request, 'quizzes/quiz_detail.html', {'quiz': quiz, 'questions': questions})
