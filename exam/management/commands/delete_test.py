from random import randint, choice

from django.core.management.base import BaseCommand
from exam.models import Question, Course, set_question_number, set_total_marks
from teacher.models import Teacher
from student.models import Student


class Command(BaseCommand):
    def handle(self, *args, **options):
        courses = Course.objects.all()
        for course in courses:
            course.delete()
