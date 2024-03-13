from django.urls import path
from student import views
from django.contrib.auth.views import LoginView

urlpatterns = [
    path('studentclick', views.studentclick_view),
    path('studentlogin', LoginView.as_view(template_name='student/studentlogin.html'), name='studentlogin'),
    path('studentsignup', views.student_signup_view, name='studentsignup'),
    path('student-dashboard', views.student_dashboard_view, name='student-dashboard'),
    path('student-exam', views.student_exam_view, name='student-exam'),
    path('take-exam/<int:pk>', views.take_exam_view, name='take-exam'),
    path('start-exam/<int:pk>', views.start_exam_view, name='start-exam'),

    path('calculate-marks', views.calculate_marks_view, name='calculate-marks'),
    path('view-result', views.view_result_view, name='view-result'),
    path('check-marks/<int:pk>', views.check_marks_view, name='check-marks'),
    path('student-marks', views.student_marks_view, name='student-marks'),

    path('update-student', views.student_update_profile, name='update-teacher'),
    path('student-change-password', views.student_change_password_view,
         name='change-password'),
    path('student-profile', views.student_profile, name='student-profile'),
    path('student-view-teachers', views.student_view_teachers_view, name='student-view-teachers'),
    path('student-view-teacher-courses/<int:pk>', views.student_view_teacher_courses_view,
         name='student-view-teacher-courses'),

]
