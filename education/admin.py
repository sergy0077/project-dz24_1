from django.contrib import admin
from .models import Course, Lesson, Payments, Subscription, EducationModeratorGroup

admin.site.register(Course)
admin.site.register(Lesson)
admin.site.register(Payments)
admin.site.register(Subscription)
admin.site.register(EducationModeratorGroup)