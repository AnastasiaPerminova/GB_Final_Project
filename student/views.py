from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

from exam import models as QMODEL
from student import forms as SFORM
from student import models as SMODEL
from teacher import models as TMODEL
from . import forms, models


def studentclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request, 'student/studentclick.html')


def student_signup_view(request):
    user_form = forms.StudentUserForm()
    student_form = forms.StudentForm()
    mydict = {'userForm': user_form, 'studentForm': student_form}
    if request.method == 'POST':
        user_form = forms.StudentUserForm(request.POST)
        student_form = forms.StudentForm(request.POST, request.FILES)
        if user_form.is_valid() and student_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            student = student_form.save(commit=False)
            student.user = user
            student.save()
            my_student_group = Group.objects.get_or_create(name='STUDENT')
            my_student_group[0].user_set.add(user)
        return HttpResponseRedirect('studentlogin')
    return render(request, 'student/studentsignup.html', context=mydict)


def is_student(user):
    return user.groups.filter(name='STUDENT').exists()


@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def student_dashboard_view(request):
    dict = {

        'total_course': QMODEL.Course.objects.all().filter(is_published=True).filter(is_deleted=False).count(),
        'total_teachers': TMODEL.Teacher.objects.all().count(),
    }
    return render(request, 'student/student_dashboard.html', context=dict)


@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def student_exam_view(request):
    courses = QMODEL.Course.objects.all().filter(is_published=True).filter(is_deleted=False)
    student = SMODEL.Student.objects.get(user_id=request.user.id)
    results = QMODEL.Result.objects.all().filter(student=student)
    attempted_courses = []
    for result in results:
        if result.exam not in attempted_courses:
            attempted_courses.append(result.exam)
    return render(request, 'student/student_exam.html', {'courses': courses, 'attempted': attempted_courses})


@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def take_exam_view(request, pk):
    course = QMODEL.Course.objects.get(id=pk)
    total_questions = QMODEL.Question.objects.all().filter(course=course).count()
    questions = QMODEL.Question.objects.all().filter(course=course)
    total_marks = 0
    for q in questions:
        total_marks = total_marks + q.marks

    return render(request, 'student/take_exam.html',
                  {'course': course, 'total_questions': total_questions, 'total_marks': total_marks})


@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def start_exam_view(request, pk):
    course = QMODEL.Course.objects.get(id=pk)
    questions = QMODEL.Question.objects.all().filter(course=course)
    if request.method == 'POST':
        pass
    response = render(request, 'student/start_exam.html', {'course': course, 'questions': questions})
    response.set_cookie('course_id', course.id)
    return response


@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def calculate_marks_view(request):
    if request.COOKIES.get('course_id') is not None:
        course_id = request.COOKIES.get('course_id')
        course = QMODEL.Course.objects.get(id=course_id)

        total_marks = 0
        questions = QMODEL.Question.objects.all().filter(course=course)
        for i in range(len(questions)):

            selected_ans = request.COOKIES.get(str(i + 1))
            actual_answer = questions[i].answer
            if selected_ans == actual_answer:
                total_marks = total_marks + questions[i].marks
        student = models.Student.objects.get(user_id=request.user.id)
        result = QMODEL.Result()
        result.marks = total_marks
        result.success_percentage = total_marks / course.total_marks * 100
        result.exam = course
        result.student = student
        result.save()

        return HttpResponseRedirect(f'check-marks/{course.id}')


@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def check_marks_view(request, pk):
    course = QMODEL.Course.objects.get(id=pk)
    student = models.Student.objects.get(user_id=request.user.id)
    results = QMODEL.Result.objects.all().filter(exam=course).filter(student=student)
    return render(request, 'student/check_marks.html', {'results': results})


@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def student_marks_view(request):
    student = SMODEL.Student.objects.get(user_id=request.user.id)
    results = QMODEL.Result.objects.all().filter(student=student)
    attempted_courses = []
    for result in results:
        if result.exam not in attempted_courses:
            attempted_courses.append(result.exam)
    return render(request, 'student/student_marks.html', {'courses': attempted_courses})


@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def student_profile(request):
    student = models.Student.objects.get(user_id=request.user.id)
    return render(request, 'student/student_profile.html', context={'student': student})


@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def student_update_profile(request):
    student = SMODEL.Student.objects.get(user_id=request.user.id)
    user = SMODEL.User.objects.get(id=student.user_id)
    if request.method == 'POST':
        user_form = SFORM.UserUpdateForm(request.POST, instance=user)
        student_form = SFORM.StudentForm(request.POST or None, request.FILES or None, instance=student)
        if user_form.is_valid() and student_form.is_valid():
            user_form.save(commit=False)
            user.save()
            student_form.save()
            student.save()
        return redirect('teacher-profile')
    else:
        user_form = SFORM.UserUpdateForm(instance=user)
        student_form = SFORM.StudentForm(instance=student)
    mydict = {'userForm': user_form, 'studentForm': student_form}
    return render(request, 'student/update_student.html', context=mydict)


@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def student_view_teachers_view(request):
    teachers = TMODEL.Teacher.objects.all()
    return render(request, 'student/student_view_teachers.html', context={'teachers': teachers})


@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def student_view_teacher_courses_view(request, pk):
    teacher = TMODEL.Teacher.objects.get(id=pk)
    courses = QMODEL.Course.objects.all().filter(teacher=teacher).filter(is_published=True).filter(is_deleted=False)
    student = SMODEL.Student.objects.get(user_id=request.user.id)

    attempted_courses = []
    for course in courses:
        if QMODEL.Result.objects.all().filter(student=student).filter(exam=course) and course not in attempted_courses:
            attempted_courses.append(course)
    return render(request, 'student/student_view_teacher_courses.html', context={'teacher': teacher, 'courses': courses,
                                                                                 'attempted': attempted_courses})


@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def student_change_password_view(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(
                request, 'Ваш пароль успешно обновлен!')

        else:
            form = PasswordChangeForm(request.user)
            messages.warning(
                request, 'Возникла ошибка при смене пароля!!')
    else:
        form = PasswordChangeForm(request.user)

    return render(request, 'student/student_password_change.html', {'form': form})
