from django.urls import path
from django.views.generic import RedirectView
from . import views

urlpatterns = [

    # =========================
    # 🏠 Home
    # =========================
    path('', views.home, name='home'),

    # =========================
    # 📝 Student Registration
    # =========================
    path('student/register/', views.student_register, name='student_register'),

    path('delete-student/<int:id>/', views.delete_student, name='delete_student'),    # Optional shortcut
    
    path(
        'register/',
        RedirectView.as_view(
            pattern_name='student_register',
            permanent=False
        )
    ),

    # =========================
    # 🔐 Student Login
    # =========================
    path('student/login/', views.student_login, name='student_login'),

    # Optional shortcut
    path(
        'login/',
        RedirectView.as_view(
            pattern_name='student_login',
            permanent=False
        )
    ),

    # =========================
    # 📋 Student Dashboard
    # =========================
    path('student/dashboard/', views.student_dashboard, name='student_dashboard'),

    # =========================
    # 🔐 Admin / Teacher Login
    # (avoid conflict with Django default /admin/)
    # =========================
    path('staff/login/', views.admin_login, name='admin_login'),

    # =========================
    # 📊 Admin Dashboard
    # =========================
    path('staff/dashboard/', views.admin_dashboard, name='admin_dashboard'),

    # =========================
    # ✅ Verify / ❌ Reject Student
    # =========================
    path(
        'staff/student/verify/<int:id>/',
        views.verify_student,
        name='verify_student'
    ),

    path(
        'staff/student/reject/<int:id>/',
        views.reject_student,
        name='reject_student'
    ),

    # =========================
    # 📋 Admin – List All Students
    # =========================
    path(
        'staff/students/',
        views.admin_students,
        name='admin_students'
    ),

    # =========================
    # 🚪 Logout (Admin / Student)
    # =========================
    path('logout/', views.user_logout, name='logout'),

]
