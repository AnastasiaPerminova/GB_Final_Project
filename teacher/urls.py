from django.contrib.auth.views import LoginView
from django.urls import path

from teacher import views

urlpatterns = [
    path('teacherclick', views.teacherclick_view),
    path('teacherlogin', LoginView.as_view(template_name='teacher/teacherlogin.html'), name='teacherlogin'),
    path('teachersignup', views.teacher_signup_view, name='teachersignup'),
    path('teacher-dashboard', views.teacher_dashboard_view, name='teacher-dashboard'),
    path('teacher-change-password', views.teacher_change_password_view,
         name='change-password'),

    path('teacher-exam', views.teacher_exam_view, name='teacher-exam'),
    path('teacher-add-exam', views.teacher_add_exam_view, name='teacher-add-exam'),
    path('teacher-view-exam', views.teacher_view_exam_view, name='teacher-view-exam'),
    path('delete-exam/<int:pk>', views.delete_exam_view, name='delete-exam'),
    path('teacher-publish-exam/<int:pk>', views.teacher_publish_exam_view, name='teacher-publish-exam'),
    path('teacher-unpublish-exam/<int:pk>', views.teacher_unpublish_exam_view, name='teacher-unpublish-exam'),

    path('teacher-question', views.teacher_question_view, name='teacher-question'),
    path('teacher-add-question-course/<int:pk>', views.teacher_add_question_course_view,
         name='teacher-add-question-course'),
    path('teacher-view-question', views.teacher_view_question_view, name='teacher-view-question'),
    path('teacher-update-question/<int:pk>', views.teacher_update_question_view, name='teacher-update-question'),
    path('see-question/<int:pk>', views.see_question_view, name='see-question'),
    path('see-full-question/<int:pk>', views.see_full_question_view, name='see-full-question'),
    path('remove-question/<int:pk>', views.remove_question_view, name='remove-question'),

    path('teacher-view-students', views.teacher_view_students_view, name='teacher-view-students'),
    path('teacher-view-student-marks/<int:pk>', views.teacher_view_student_marks_view, name='teacher-view-student-marks'),
    path('teacher-check-student-marks/<int:pk>', views.teacher_сheck_student_marks_view,
         name='teacher-check-student-marks'),
    path('teacher-view-course-marks/<int:pk>', views.teacher_view_course_marks_view, name='teacher-view-course-marks'),

    path('update-teacher', views.teacher_update_profile, name='update-teacher'),
    path('teacher-profile', views.teacher_profile, name='teacher-profile'),


]
