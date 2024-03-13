from django.urls import path, include, reverse_lazy
from django.contrib import admin
from exam import views
from django.contrib.auth.views import LogoutView, LoginView, PasswordChangeView, PasswordChangeDoneView

from django.conf.urls.static import static

urlpatterns = [

    path('admin/', admin.site.urls),
    path('teacher/', include('teacher.urls')),
    path('student/', include('student.urls')),



    path('', views.home_view, name=''),
    path('logout', views.user_logout_view, name='logout'),
    path('contactus', views.contactus_view),
    path('afterlogin', views.afterlogin_view, name='afterlogin'),
    path('change-password', views.admin_change_password_view,
         name='change-password'),

    path('adminclick', views.adminclick_view),
    path('adminlogin', LoginView.as_view(template_name='exam/adminlogin.html'), name='adminlogin'),
    path('admin-dashboard', views.admin_dashboard_view, name='admin-dashboard'),
    path('admin-teacher', views.admin_teacher_view, name='admin-teacher'),
    path('admin-view-teacher', views.admin_view_teacher_view, name='admin-view-teacher'),
    path('update-teacher/<int:pk>', views.update_teacher_view, name='update-teacher'),
    path('admin-change-teacher-password/<int:pk>', views.admin_change_teacher_password_view,
         name='admin-change-teacher-password'),
    path('delete-teacher/<int:pk>', views.delete_teacher_view, name='delete-teacher'),
    path('disable-teacher/<int:pk>', views.disable_teacher_view, name='disable-teacher'),
    path('activate-teacher/<int:pk>', views.activate_teacher_view, name='activate-teacher'),
    path('admin-view-pending-teacher', views.admin_view_pending_teacher_view, name='admin-view-pending-teacher'),
    path('approve-teacher/<int:pk>', views.approve_teacher_view, name='approve-teacher'),
    path('reject-teacher/<int:pk>', views.reject_teacher_view, name='reject-teacher'),

    path('admin-student', views.admin_student_view, name='admin-student'),
    path('admin-view-student', views.admin_view_student_view, name='admin-view-student'),
    path('admin-view-student-marks', views.admin_view_student_marks_view, name='admin-view-student-marks'),
    path('admin-view-marks/<int:pk>', views.admin_view_marks_view, name='admin-view-marks'),
    path('admin-check-marks/<int:pk>', views.admin_check_marks_view, name='admin-check-marks'),
    path('update-student/<int:pk>', views.update_student_view, name='update-student'),
    path('admin-change-student-password/<int:pk>', views.admin_change_student_password_view,
         name='admin-change-student-password'),
    path('delete-student/<int:pk>', views.delete_student_view, name='delete-student'),
    path('disable-student/<int:pk>', views.disable_student_view, name='disable-student'),
    path('activate-student/<int:pk>', views.activate_student_view, name='activate-student'),

    path('admin-course', views.admin_course_view, name='admin-course'),
    path('admin-add-course', views.admin_add_course_view, name='admin-add-course'),
    path('admin-view-course', views.admin_view_course_view, name='admin-view-course'),
    path('delete-course/<int:pk>', views.delete_course_view, name='delete-course'),
    path('disable-course/<int:pk>', views.disable_course_view, name='disable-course'),
    path('activate-course/<int:pk>', views.activate_course_view, name='activate-course'),
    path('admin-view-course-marks/<int:pk>', views.admin_view_course_marks_view, name='admin-view-course-marks'),

    path('admin-question', views.admin_question_view, name='admin-question'),
    path('admin-add-question', views.admin_add_question_view, name='admin-add-question'),
    path('admin-view-question', views.admin_view_question_view, name='admin-view-question'),
    path('admin-see-question/<int:pk>', views.admin_see_question_view, name='admin-see-question'),
    path('admin-update-question/<int:pk>', views.admin_update_question_view, name='admin-update-question'),
    path('view-question/<int:pk>', views.view_question_view, name='view-question'),
    path('admin-see-full-question/<int:pk>', views.admin_see_full_question_view, name='admin-see-full-question'),
    path('admin-delete-question/<int:pk>', views.delete_question_view, name='admin-delete-question'),
    path('disable-question/<int:pk>', views.disable_question_view, name='disable-question'),
    path('activate-question/<int:pk>', views.activate_question_view, name='activate-question'),

]
