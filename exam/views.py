from django.conf import settings
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404

from student import forms as SFORM
from student import models as SMODEL
from teacher import forms as TFORM
from teacher import models as TMODEL
from . import forms, models


def home_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request, 'exam/index.html')


def is_teacher(user):
    """

    Проверка при аутентификации пользователя, является ли он Учителем.

    """
    return user.groups.filter(name='TEACHER').exists()


def is_student(user):
    """

    Проверка при аутентификации пользователя, является ли он Студентом.

    """
    return user.groups.filter(name='STUDENT').exists()


def is_staff(user):
    """

    Проверка при аутентификации пользователя, обладает ли он правами администратора.

    """
    return user.is_staff


@login_required
def user_logout_view(request):
    """

    Страница после  перехода по кнопке "Выйти"

    """
    logout(request)
    return render(request, 'exam/logout.html', {})


def afterlogin_view(request):
    """

    Страница после  авторизации пользователя.

    """
    if is_student(request.user):
        return redirect('student/student-dashboard')

    elif is_teacher(request.user):
        accountapproval = TMODEL.Teacher.objects.all().filter(user_id=request.user.id, status=True)
        if accountapproval:
            return redirect('teacher/teacher-dashboard')
        else:
            return render(request, 'teacher/teacher_wait_for_approval.html')

    elif is_staff(request.user):
        return redirect('admin-dashboard')


def adminclick_view(request):
    """

    Кнопка "Администратор" в шапке главной страницы.

    """
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return HttpResponseRedirect('adminlogin')


@login_required(login_url='adminlogin')
@user_passes_test(is_staff)
def admin_dashboard_view(request):
    """

    Главная страница пользователя - Администратор после аутентификации.

    """
    dict = {
        'total_student': SMODEL.Student.objects.all().count(),
        'total_teacher': TMODEL.Teacher.objects.all().filter(status=True).count(),
        'total_course': models.Course.objects.all().count(),
        'total_question': models.Question.objects.all().count(),
    }
    return render(request, 'exam/admin_dashboard.html', context=dict)


@login_required(login_url='adminlogin')
@user_passes_test(is_staff)
def admin_teacher_view(request):
    """

    Учителя.

    """
    dict = {
        'total_teacher': TMODEL.Teacher.objects.all().filter(status=True).count(),
        'pending_teacher': TMODEL.Teacher.objects.all().filter(status=False).count(),
    }
    return render(request, 'exam/admin_teacher.html', context=dict)


@login_required(login_url='adminlogin')
@user_passes_test(is_staff)
def admin_view_teacher_view(request):
    """

    Все зарегистрированные учителя.

    """
    teachers = TMODEL.Teacher.objects.all().filter(status=True)
    return render(request, 'exam/admin_view_teacher.html', {'teachers': teachers})


@login_required(login_url='adminlogin')
@user_passes_test(is_staff)
def update_teacher_view(request, pk):
    """

    Редактировать информацию в профиле Учителя.

    """
    teacher = TMODEL.Teacher.objects.get(id=pk)
    user = TMODEL.User.objects.get(id=teacher.user_id)
    if request.method == 'POST':
        user_form = TFORM.UserUpdateForm(request.POST, instance=user)
        teacher_form = TFORM.TeacherForm(request.POST or None, request.FILES or None, instance=teacher)
        if user_form.is_valid() and teacher_form.is_valid():
            user_form.save(commit=False)
            user.save()
            teacher_form.save()
            teacher.save()
        return redirect('/admin-view-teacher')
    else:
        user_form = TFORM.UserUpdateForm(instance=user)
        teacher_form = TFORM.TeacherForm(instance=teacher)
    mydict = {'userForm': user_form, 'teacherForm': teacher_form, 'teacher': teacher}
    return render(request, 'exam/update_teacher.html', context=mydict)


@login_required(login_url='adminlogin')
@user_passes_test(is_staff)
def admin_change_teacher_password_view(request, pk):
    """

    Смена пароля в профиле Учителя.

    """
    teacher = TMODEL.Teacher.objects.get(id=pk)
    user = teacher.user

    if request.method == 'POST':
        form = SFORM.UserAdminChangePassword(request.POST, instance=user)
        if form.is_valid():
            form.save()
            user.set_password(user.password)
            user.save()
            messages.success(
                request, 'Пароль успешно обновлен!')

        else:
            form = SFORM.UserAdminChangePassword(instance=user)
            messages.warning(
                request, 'Возникла ошибка при смене пароля!!')
    else:
        form = SFORM.UserAdminChangePassword(instance=user)

    return render(request, 'exam/admin_change_teacher_password.html', {'form': form, 'user': user})


@login_required(login_url='adminlogin')
@user_passes_test(is_staff)
def disable_teacher_view(request, pk):
    """

    Отключить аккаунт Учителя.

    """
    teacher = TMODEL.Teacher.objects.get(id=pk)
    user = User.objects.get(id=teacher.user_id)
    user.is_active = False
    user.save()
    return HttpResponseRedirect('/admin-view-teacher')


@login_required(login_url='adminlogin')
@user_passes_test(is_staff)
def activate_teacher_view(request, pk):
    """

    Активировать аккаунт Учителя.

    """
    teacher = TMODEL.Teacher.objects.get(id=pk)
    user = User.objects.get(id=teacher.user_id)
    user.is_active = True
    user.save()
    return HttpResponseRedirect('/admin-view-teacher')


@login_required(login_url='adminlogin')
@user_passes_test(is_staff)
def delete_teacher_view(request, pk):
    """

    Удалить аккаунт Учителя из Базы Данных.

    """

    teacher = TMODEL.Teacher.objects.get(id=pk)
    user = User.objects.get(id=teacher.user_id)
    user.delete()
    teacher.delete()
    return HttpResponseRedirect('/admin-view-teacher')


@login_required(login_url='adminlogin')
@user_passes_test(is_staff)
def admin_view_pending_teacher_view(request):
    """

    Просмотр учителей, ожидающих авторизации.

    """
    teachers = TMODEL.Teacher.objects.all().filter(status=False)
    return render(request, 'exam/admin_view_pending_teacher.html', {'teachers': teachers})


@login_required(login_url='adminlogin')
@user_passes_test(is_staff)
def approve_teacher_view(request, pk):
    """

    Подтверждение авторизации учителя.

    """
    teacher = TMODEL.Teacher.objects.get(id=pk)
    teacher.status = True
    teacher.save()
    return HttpResponseRedirect('/admin-view-pending-teacher')


@login_required(login_url='adminlogin')
@user_passes_test(is_staff)
def reject_teacher_view(request, pk):
    """

    Отклонение авторизации учителя.

    """
    teacher = TMODEL.Teacher.objects.get(id=pk)
    user = User.objects.get(id=teacher.user_id)
    user.delete()
    teacher.delete()
    return HttpResponseRedirect('/admin-view-pending-teacher')


@login_required(login_url='adminlogin')
@user_passes_test(is_staff)
def admin_student_view(request):
    """

    Кнопка студенты боковой панели.

    """
    dict = {
        'total_student': SMODEL.Student.objects.all().count(),
    }
    return render(request, 'exam/admin_student.html', context=dict)


@login_required(login_url='adminlogin')
@user_passes_test(is_staff)
def admin_view_student_view(request):
    """

    Список всех студентов.

    """
    students = SMODEL.Student.objects.all()
    return render(request, 'exam/admin_view_student.html', {'students': students})


@login_required(login_url='adminlogin')
@user_passes_test(is_staff)
def update_student_view(request, pk):
    """

    Редактировать информацию в профиле Студента.

    """
    student = SMODEL.Student.objects.get(id=pk)
    user = SMODEL.User.objects.get(id=student.user_id)
    if request.method == 'POST':
        user_form = SFORM.UserUpdateForm(request.POST, instance=user)
        student_form = SFORM.StudentForm(request.POST, request.FILES, instance=student)
        if user_form.is_valid() and student_form.is_valid():
            user_form.save()
            user.save()
            student_form.save()
            student.save()
        return HttpResponseRedirect('/admin-view-student')
    else:
        user_form = SFORM.UserUpdateForm(instance=user)
        student_form = SFORM.StudentForm(instance=student)
    mydict = {'userForm': user_form, 'studentForm': student_form, 'student': student}
    return render(request, 'exam/update_student.html', context=mydict)


@login_required(login_url='adminlogin')
@user_passes_test(is_staff)
def admin_change_student_password_view(request, pk):
    """

    Смена пароля в профиле Студента.

    """
    student = SMODEL.Student.objects.get(id=pk)
    user = student.user

    if request.method == 'POST':
        form = SFORM.UserAdminChangePassword(request.POST, instance=user)
        if form.is_valid():
            form.save()
            user.set_password(user.password)
            user.save()
            messages.success(
                request, 'Ваш пароль успешно обновлен!')

        else:
            form = SFORM.UserAdminChangePassword(instance=user)
            messages.warning(
                request, 'Возникла ошибка при смене пароля!!')
    else:
        form = SFORM.UserAdminChangePassword(instance=user)

    return render(request, 'exam/admin_change_student_password.html', {'form': form, 'user': user})


@login_required(login_url='adminlogin')
@user_passes_test(is_staff)
def disable_student_view(request, pk):
    """

    Отключить аккаунт Студента.

    """
    student = SMODEL.Student.objects.get(id=pk)
    user = User.objects.get(id=student.user_id)
    user.is_active = False
    user.save()
    return HttpResponseRedirect('/admin-view-student')


@login_required(login_url='adminlogin')
@user_passes_test(is_staff)
def activate_student_view(request, pk):
    """

    Активировать аккаунт Студента.

    """
    student = SMODEL.Student.objects.get(id=pk)
    user = User.objects.get(id=student.user_id)
    user.is_active = True
    user.save()
    return HttpResponseRedirect('/admin-view-student')


@login_required(login_url='adminlogin')
@user_passes_test(is_staff)
def delete_student_view(request, pk):
    """

    Удалить аккаунт Студента из Базы Данных.

    """
    student = SMODEL.Student.objects.get(id=pk)
    user = User.objects.get(id=student.user_id)
    user.delete()
    student.delete()
    return HttpResponseRedirect('/admin-view-student')


@login_required(login_url='adminlogin')
@user_passes_test(is_staff)
def admin_course_view(request):
    """

    Кнопка Тесты боковой панели.

    """
    return render(request, 'exam/admin_course.html')


@login_required(login_url='adminlogin')
@user_passes_test(is_staff)
def admin_add_course_view(request):
    """

    Добавить тест.

    """
    course_form = forms.CourseForm()
    if request.method == 'POST':
        course_form = forms.CourseForm(request.POST)
        if course_form.is_valid():
            course_form.save()

        else:
            print("form is invalid")
        return HttpResponseRedirect('/admin-view-course')
    return render(request, 'exam/admin_add_course.html', {'courseForm': course_form})


@login_required(login_url='adminlogin')
@user_passes_test(is_staff)
def admin_view_course_view(request):
    """

    Список всех тестов.

    """
    courses = models.Course.objects.all()
    return render(request, 'exam/admin_view_course.html', {'courses': courses})


@login_required(login_url='adminlogin')
@user_passes_test(is_staff)
def delete_course_view(request, pk):
    """

    Удалить тест из Базы Данных.

    """
    course = models.Course.objects.get(id=pk)
    course.delete()
    return HttpResponseRedirect('/admin-view-course')


@login_required(login_url='adminlogin')
@user_passes_test(is_staff)
def disable_course_view(request, pk):
    """

    Отключить тест.

    """
    course = models.Course.objects.get(id=pk)
    course.is_deleted = True
    course.save()
    questions = models.Question.objects.all().filter(course=course)
    for question in questions:
        question.is_deleted = True
        question.save()
    return HttpResponseRedirect('/admin-view-course')


@login_required(login_url='adminlogin')
@user_passes_test(is_staff)
def activate_course_view(request, pk):
    """

    Активировать тест.

    """
    course = models.Course.objects.get(id=pk)
    course.is_deleted = False
    course.save()
    questions = models.Question.objects.all().filter(course=course)
    for question in questions:
        question.is_deleted = False
        question.save()
    return HttpResponseRedirect('/admin-view-course')


@login_required(login_url='adminlogin')
@user_passes_test(is_staff)
def admin_question_view(request):
    """

    Кнопка вопросы боковой панели.

    """
    return render(request, 'exam/admin_question.html')


@login_required(login_url='adminlogin')
@user_passes_test(is_staff)
def admin_see_question_view(request, pk):
    """

    Список вопросов по конкретному тесту.

    """
    course = models.Course.objects.get(id=pk)
    questions = models.Question.objects.all().filter(course_id=pk)
    return render(request, 'exam/admin_see_question.html', {'questions': questions, 'course': course})


@login_required(login_url='adminlogin')
@user_passes_test(is_staff)
def admin_add_question_view(request):
    """Администратор добавляет вопрос."""
    question_form = forms.AdminQuestionForm()
    if request.method == 'POST':
        question_form = forms.AdminQuestionForm(request.POST)
        if question_form.is_valid():
            question = question_form.save(commit=False)
            course = models.Course.objects.get(id=request.POST.get('courseID'))
            question.course = course
            question.save()
        else:
            print("form is invalid")
        return HttpResponseRedirect('/admin-view-question')
    return render(request, 'exam/admin_add_question.html', {'questionForm': question_form})


@login_required(login_url='adminlogin')
@user_passes_test(is_staff)
def admin_view_question_view(request):
    """

    Список всех вопросов.

    """
    questions = models.Question.objects.all()
    return render(request, 'exam/admin_view_question.html', {'questions': questions})


@login_required(login_url='adminlogin')
@user_passes_test(is_staff)
def view_question_view(request, pk):
    """

    Список вопросов по конкретному тесту.

    """
    questions = models.Question.objects.all().filter(course_id=pk)
    return render(request, 'exam/view_question.html', {'questions': questions})


@login_required(login_url='adminlogin')
@user_passes_test(is_staff)
def admin_see_full_question_view(request, pk):
    """
    Просмотр подробной информации о вопросе.

    """
    question = get_object_or_404(models.Question, pk=pk)
    return render(request, 'exam/see_full_question.html', {'question': question})


@login_required(login_url='adminlogin')
@user_passes_test(is_staff)
def admin_update_question_view(request, pk):
    """

    Редактирование вопроса.

    """
    question_id = pk
    question = models.Question.objects.get(id=question_id)
    course = question.course
    question_form = forms.AdminUpdateQuestionForm(instance=question)
    if request.method == 'POST':
        question_form = forms.AdminUpdateQuestionForm(request.POST, instance=question)
        if question_form.is_valid():
            question_form.save(commit=False)
            question.save()
            if models.Course.objects.get(id=request.POST.get('courseID')):
                course = models.Course.objects.get(id=request.POST.get('courseID'))
                question.course = course
                question.save()
            course = question.course
            models.set_question_number(course)
            models.set_total_marks(course)
            course.is_published = False
            course.save()
        else:
            print("form is invalid")
        return HttpResponseRedirect(f'/admin/see-question/{course.id}')
    return render(request, 'exam/admin_update_question.html', {'questionForm': question_form})


@login_required(login_url='adminlogin')
@user_passes_test(is_staff)
def delete_question_view(request, pk):
    """

    Удалить Вопрос из Базы Данных.

    """
    question = models.Question.objects.get(id=pk)
    question.delete()
    return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))


@login_required(login_url='adminlogin')
@user_passes_test(is_staff)
def disable_question_view(request, pk):
    """

    Отключить Вопрос.

    """

    question = models.Question.objects.get(id=pk)
    question.is_deleted = True
    question.save()
    return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))


@login_required(login_url='adminlogin')
@user_passes_test(is_staff)
def activate_question_view(request, pk):
    """

    Включить  Вопрос.

     """
    question = models.Question.objects.get(id=pk)
    question.is_deleted = False
    question.save()
    return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))


@login_required(login_url='adminlogin')
@user_passes_test(is_staff)
def admin_view_student_marks_view(request):
    """

    Просмотр результатов.

     """
    students = SMODEL.Student.objects.all()
    return render(request, 'exam/admin_view_student_marks.html', {'students': students})


@login_required(login_url='adminlogin')
@user_passes_test(is_staff)
def admin_view_marks_view(request, pk):
    """

    Список тестов с резузльтатами

    """
    courses = models.Course.objects.all()
    response = render(request, 'exam/admin_view_marks.html', {'courses': courses})
    response.set_cookie('student_id', str(pk))
    return response


@login_required(login_url='adminlogin')
@user_passes_test(is_staff)
def admin_check_marks_view(request, pk):
    """

    Результаты конкретного теста у конкретного студента.

    """
    course = models.Course.objects.get(id=pk)
    student_id = request.COOKIES.get('student_id')
    student = SMODEL.Student.objects.get(id=student_id)

    results = models.Result.objects.all().filter(exam=course).filter(student=student)
    return render(request, 'exam/admin_check_marks.html', {'results': results})


@login_required(login_url='adminlogin')
@user_passes_test(is_staff)
def admin_view_course_marks_view(request, pk):
    """

    Результаты конкретного теста.

    """
    course = models.Course.objects.get(id=pk)
    results = models.Result.objects.all().filter(exam=course)
    return render(request, 'exam/admin-view-course-marks.html', {'results': results})


@login_required(login_url='adminlogin')
@user_passes_test(is_staff)
def admin_change_password_view(request):
    """

    Смена пароля администратора.

    """
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

    return render(request, 'exam/admin_password_change.html', {'form': form})


def contactus_view(request):
    """
    Контакты. Форма обратной связи.

    """
    sub = forms.ContactusForm()
    if request.method == 'POST':
        sub = forms.ContactusForm(request.POST)
        if sub.is_valid():
            email = sub.cleaned_data['Email']
            name = sub.cleaned_data['Name']
            message = sub.cleaned_data['Message']
            send_mail(str(name) + ' || ' + str(email), message, settings.EMAIL_HOST_USER, settings.EMAIL_RECEIVING_USER,
                      fail_silently=False)
            return render(request, 'exam/contactussuccess.html')
    return render(request, 'exam/contactus.html', {'form': sub})
