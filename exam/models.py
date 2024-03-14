from django.db import models
from student.models import Student
from teacher.models import Teacher


class Course(models.Model):
    course_name = models.CharField(max_length=50)
    question_number = models.PositiveIntegerField(default=0)
    total_marks = models.PositiveIntegerField(default=0)
    teacher = models.ForeignKey(Teacher, null=True, on_delete=models.CASCADE)
    is_published = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.teacher.get_name} + " {self.course_name}"'

    def __repr__(self):
        return f'{self.teacher.get_name} + " {self.course_name}"'


class Question(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    marks = models.PositiveIntegerField()
    question = models.CharField(max_length=600)
    option1 = models.CharField(max_length=200)
    option2 = models.CharField(max_length=200)
    option3 = models.CharField(max_length=200)
    option4 = models.CharField(max_length=200)
    cat = (('Вариант 1', 'Вариант 1'), ('Вариант 2', 'Вариант 2'),
           ('Вариант 3', 'Вариант 3'), ('Вариант 4', 'Вариант 4'))
    answer = models.CharField(max_length=200, choices=cat)
    is_deleted = models.BooleanField(default=False)


def set_question_number(course):
    course.question_number = Question.objects.all().filter(course=course).count()
    course.save()
    return course.question_number


def set_total_marks(course):
    questions = Question.objects.all().filter(course=course)
    course.total_marks = 0
    for q in questions:
        course.total_marks += q.marks
    course.save()
    return course.total_marks


class Result(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    exam = models.ForeignKey(Course, on_delete=models.CASCADE)
    marks = models.PositiveIntegerField()
    success_percentage = models.PositiveIntegerField(blank=True, default=0)
    date = models.DateTimeField(auto_now=True)
