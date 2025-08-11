from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

class Course(models.Model):
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    instructor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='courses_taught')
    title = models.CharField(max_length=200)
    description = models.TextField()
    thumbnail = models.ImageField(upload_to='course_thumbnails/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Enrollment(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    enrolled_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'course')

    def __str__(self):
        return f'{self.student.username} enrolled in {self.course.title}'

class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=200)
    lesson_number = models.PositiveIntegerField()
    video_file = models.FileField(upload_to='lesson_videos/', blank=True, null=True)
    content = models.TextField()

    class Meta:
        ordering = ['lesson_number']
        unique_together = ('course', 'lesson_number')

    def __str__(self):
        return f'{self.course.title} - Lesson {self.lesson_number}: {self.title}'

class Resource(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='resources')
    title = models.CharField(max_length=200)
    file = models.FileField(upload_to='lesson_resources/')

    def __str__(self):
        return self.title
