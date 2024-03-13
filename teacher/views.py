from django.contrib import messages
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404

from exam import forms as QFORM
from exam import models as QMODEL
from student import models as SMODEL
from teacher import forms as TFORM
from teacher import models as TMODEL
from . import forms, models


# for showing signup/login button for teacher
def teacherclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request, 'teacher/teacherclick.html')


def teacher_signup_view(request):
    if request.method == 'POST':
        user_form = forms.UserForm(request.POST)
        teacher_form = forms.TeacherForm(request.POST, request.FILES)
        message = 'Ошибка в данных'
        if user_form.is_valid() and teacher_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            teacher = teacher_form.save(commit=False)
            teacher.user = user
            teacher.save()
            my_teacher_group = Group.objects.get_or_create(name='TEACHER')
            my_teacher_group[0].user_set.add(user)
            message = 'Пользователь успешно сохранён'

    else:
        user_form = forms.UserForm()
        teacher_form = forms.TeacherForm()
        message = 'Заполните форму'
    return render(request, 'teacher/teachersignup.html', context={'userForm': user_form, 'teacherForm': teacher_form,
                                                                  'message': message})


def is_teacher(user):
    return user.groups.filter(name='TEACHER').exists()


@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def teacher_dashboard_view(request):
    teacher = models.Teacher.objects.get(user_id=request.user.id)
    courses = QMODEL.Course.objects.all().filter(teacher=teacher)
    courses_q = QMODEL.Course.objects.all().filter(teacher=teacher).filter(is_deleted=False)
    questions = 0
    students = []
    for course in courses_q:
        questions += QMODEL.Question.objects.all().filter(course=course).filter(is_deleted=False).count()

    for course in courses:
        results = QMODEL.Result.objects.all().filter(exam=course)
        for res in results:
            if res.student not in students:
                students.append(res.student)

    dict = {
        'total_course': courses.count(),
        'total_question': questions,
        'total_student': len(students)
    }
    return render(request, 'teacher/teacher_dashboard.html', context=dict)


@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def teacher_view_students_view(request):
    teacher = models.Teacher.objects.get(user_id=request.user.id)
    courses = QMODEL.Course.objects.all().filter(teacher=teacher)
    students = []
    for course in courses:
        results = QMODEL.Result.objects.all().filter(exam=course)
        for res in results:
            if res.student not in students:
                students.append(res.student)
    return render(request, 'teacher/teacher_view_students.html', {'students': students})


@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def teacher_view_student_marks_view(request, pk):
    teacher = models.Teacher.objects.get(user_id=request.user.id)
    student = SMODEL.Student.objects.get(id=pk)
    courses = QMODEL.Course.objects.all().filter(teacher=teacher)
    teacher_courses = []
    for course in courses:
        if QMODEL.Result.objects.all().filter(student=student).filter(exam=course):
            teacher_courses.append(course)
    response = render(request, 'teacher/teacher_view_student_marks.html', {'student': student,
                                                                           'courses': teacher_courses})
    response.set_cookie('student_id', str(pk))
    return response


@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def teacher_сheck_student_marks_view(request, pk):
    course = QMODEL.Course.objects.get(id=pk)
    student_id = request.COOKIES.get('student_id')
    student = SMODEL.Student.objects.get(id=student_id)
    results = QMODEL.Result.objects.all().filter(exam=course).filter(student=student)
    return render(request, 'teacher/teacher_check_student_marks.html', {'results': results,
                                                                        'student': student,
                                                                        'course': course})


@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def teacher_exam_view(request):
    return render(request, 'teacher/teacher_exam.html')


@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def teacher_view_exam_view(request):
    teacher = models.Teacher.objects.get(user_id=request.user.id)
    courses = QMODEL.Course.objects.all().filter(teacher=teacher).filter(is_deleted=False)
    return render(request, 'teacher/teacher_view_exam.html', {'courses': courses})


@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def teacher_add_exam_view(request):
    course_form = QFORM.CourseForm()
    if request.method == 'POST':
        course_form = QFORM.CourseForm(request.POST)
        if course_form.is_valid():
            course = course_form.save(commit=False)
            teacher = models.Teacher.objects.get(user_id=request.user.id)
            course.teacher = teacher
            course.save()

        else:
            print("form is invalid")
        return HttpResponseRedirect('/teacher/teacher-view-exam')
    return render(request, 'teacher/teacher_add_exam.html', {'courseForm': course_form})


@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def teacher_publish_exam_view(request, pk):
    course = QMODEL.Course.objects.get(id=pk)
    course.is_published = True
    course.save()
    return HttpResponseRedirect('/teacher/teacher-view-exam')


@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def teacher_unpublish_exam_view(request, pk):
    course = QMODEL.Course.objects.get(id=pk)
    course.is_published = False
    course.save()
    return HttpResponseRedirect('/teacher/teacher-view-exam')


@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def teacher_view_course_marks_view(request, pk):
    course = QMODEL.Course.objects.get(id=pk)
    results = QMODEL.Result.objects.all().filter(course=course)
    return render(request, 'teacher/teacher-view-course-marks.html', {'results': results})


@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def delete_exam_view(request, pk):
    course = QMODEL.Course.objects.get(id=pk)
    course.is_deleted = True
    course.save()
    questions = QMODEL.Question.objects.all().filter(course=course)
    for question in questions:
        question.is_deleted = True
        question.save()
    return HttpResponseRedirect('/teacher/teacher-view-exam')


@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def teacher_question_view(request):
    return render(request, 'teacher/teacher_question.html')


@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def teacher_update_question_view(request, pk):
    question_id = pk
    question = QMODEL.Question.objects.get(id=question_id)
    course = question.course
    question_form = QFORM.TeacherQuestionForm(instance=question)
    if request.method == 'POST':
        question_form = QFORM.TeacherQuestionForm(request.POST, instance=question)
        if question_form.is_valid():
            question_form.save(commit=False)
            question.save()
            course = question.course
            QMODEL.set_question_number(course)
            QMODEL.set_total_marks(course)
            course.is_published = False
            course.save()
        else:
            print("form is invalid")
        return HttpResponseRedirect(f'/teacher/see-question/{course.id}')
    return render(request, 'teacher/teacher_update_question.html', {'questionForm': question_form})


@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def teacher_add_question_course_view(request, pk):
    question_form = QFORM.TeacherQuestionForm()
    course = QMODEL.Course.objects.get(id=pk)
    if request.method == 'POST':
        question_form = QFORM.TeacherQuestionForm(request.POST)
        if question_form.is_valid():
            question = question_form.save(commit=False)
            question.course = course
            question.save()
            QMODEL.set_question_number(course)
            QMODEL.set_total_marks(course)
            course.is_published = False
            course.save()
        else:
            print("form is invalid")
        return HttpResponseRedirect('/teacher/teacher-view-exam')
    return render(request, 'teacher/teacher_add_question_course.html', {'questionForm': question_form})


@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def teacher_view_question_view(request):
    teacher = models.Teacher.objects.get(user_id=request.user.id)
    courses = QMODEL.Course.objects.all().filter(teacher=teacher).filter(is_deleted=False)
    all_questions = []
    for course in courses:
        questions = QMODEL.Question.objects.all().filter(course=course).filter(is_deleted=False)
        for question in questions:
            all_questions.append(question)

    return render(request, 'teacher/teacher_view_question.html', {'questions': all_questions})


@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def see_question_view(request, pk):
    course = QMODEL.Course.objects.get(id=pk)
    questions = QMODEL.Question.objects.all().filter(course_id=pk)

    return render(request, 'teacher/see_question.html', {'questions': questions, 'course': course})


@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def see_full_question_view(request, pk):
    question = get_object_or_404(QMODEL.Question, pk=pk)
    return render(request, 'teacher/see_full_question.html', {'question': question})


@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def remove_question_view(request, pk):
    question = QMODEL.Question.objects.get(id=pk)
    question.course.is_published = False
    question.course.save()
    question.is_deleted = True
    question.save()
    return HttpResponseRedirect('/teacher/teacher-view-question')


@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def teacher_update_profile(request):
    teacher = models.Teacher.objects.get(user_id=request.user.id)
    user = TMODEL.User.objects.get(id=teacher.user_id)
    if request.method == 'POST':
        user_form = TFORM.UserUpdateForm(request.POST, instance=user)
        teacher_form = TFORM.TeacherForm(request.POST or None, request.FILES or None, instance=teacher)
        if user_form.is_valid() and teacher_form.is_valid():
            user_form.save(commit=False)
            user.save()
            teacher_form.save()
            teacher.save()
        return redirect('teacher-profile')
    else:
        user_form = TFORM.UserUpdateForm(instance=user)
        teacher_form = TFORM.TeacherForm(instance=teacher)
    mydict = {'userForm': user_form, 'teacherForm': teacher_form}
    return render(request, 'teacher/update_teacher.html', context=mydict)


@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def teacher_profile(request):
    teacher = models.Teacher.objects.get(user_id=request.user.id)
    return render(request, 'teacher/teacher_profile.html', context={'teacher': teacher})


@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def teacher_change_password_view(request):
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

    return render(request, 'teacher/teacher_password_change.html', {'form': form})
