from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView
from .models import Course, Enrollment, Lesson
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views import View

class CourseListView(ListView):
    model = Course
    template_name = 'courses/course_list.html'
    context_object_name = 'courses'

class CourseDetailView(DetailView):
    model = Course
    template_name = 'courses/course_detail.html'
    context_object_name = 'course'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['is_enrolled'] = Enrollment.objects.filter(student=self.request.user, course=self.object).exists()
        else:
            context['is_enrolled'] = False
        return context

class EnrollView(LoginRequiredMixin, View):
    def post(self, request, course_id):
        course = get_object_or_404(Course, id=course_id)
        Enrollment.objects.get_or_create(student=request.user, course=course)
        return redirect('courses:course_detail', pk=course_id)

class LessonDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Lesson
    template_name = 'courses/lesson_detail.html'
    context_object_name = 'lesson'

    def test_func(self):
        lesson = self.get_object()
        return Enrollment.objects.filter(student=self.request.user, course=lesson.course).exists()
