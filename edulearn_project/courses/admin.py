from django.contrib import admin
from .models import Category, Course, Enrollment, Lesson, Resource

admin.site.register(Category)
admin.site.register(Course)
admin.site.register(Enrollment)
admin.site.register(Lesson)
admin.site.register(Resource)
