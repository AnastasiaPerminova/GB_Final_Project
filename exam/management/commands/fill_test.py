from random import randint, choice

from django.core.management.base import BaseCommand
from exam.models import Question, Course, set_question_number, set_total_marks
from teacher.models import Teacher
from student.models import Student


class Command(BaseCommand):
    def handle(self, *args, **options):
        teachers = Teacher.objects.all()
        for teacher in teachers:
            n = 1
            for _ in range(10):
                course = Course(
                    teacher=teacher, course_name=f'Test{n}', is_published=True
                )
                course.save()
                n += 1
        courses = Course.objects.all()
        for course in courses:
            n = 0
            for _ in range(randint(5, 10)):
                question = Question(course=course, question=f'Question {n}', marks=randint(5, 10), option1='1',
                                    option2='2', option3='3', option4='4',
                                    answer=choice(('Вариант 1', 'Вариант 2', 'Вариант 3', 'Вариант 4')))
                question.save()
                n += 1
            set_total_marks(course)
            set_question_number(course)

