from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Student


# =========================
# 🏠 Home Page
# =========================
def home(request):
    return render(request, 'core/index.html')


# =========================
# 📝 Student Registration
# =========================
def student_register(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        dob = request.POST.get('dob')
        age = request.POST.get('age')
        gender = request.POST.get('gender', 'Male')
        course = request.POST.get('course', 'MCA')
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        previous_marks = request.POST.get('previous_marks')

        # 🔹 Validation
        if not all([username, email, password, dob, age, address, phone, previous_marks]):
            return render(request, 'core/register.html', {
                'error': 'All fields are required'
            })

        if User.objects.filter(username=username).exists():
            return render(request, 'core/register.html', {
                'error': 'Username already exists'
            })

        if User.objects.filter(email=email).exists():
            return render(request, 'core/register.html', {
                'error': 'Email already exists'
            })

        try:
            age = int(age)
            previous_marks = float(previous_marks)
        except ValueError:
            return render(request, 'core/register.html', {
                'error': 'Age must be number and marks must be numeric'
            })

        # 🔹 Create User
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        # 🔹 Create Student
        Student.objects.create(
            user=user,
            dob=dob,
            age=age,
            gender=gender,
            course=course,
            address=address,
            phone=phone,
            previous_marks=previous_marks,
            status='pending'
        )

        return redirect('student_login')

    return render(request, 'core/register.html')


# =========================
# 🔐 Student Login
# =========================
def student_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            try:
                Student.objects.get(user=user)
                login(request, user)
                return redirect('student_dashboard')
            except Student.DoesNotExist:
                pass

        return render(request, 'core/student_login.html', {
            'error': 'Invalid student credentials'
        })

    return render(request, 'core/student_login.html')


# =========================
# 📋 Student Dashboard
# =========================
@login_required
def student_dashboard(request):
    student = get_object_or_404(Student, user=request.user)
    return render(request, 'core/student_dashboard.html', {
        'student': student
    })


# =========================
# 🔐 Admin / Teacher Login
# =========================
def admin_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None and user.is_staff:
            login(request, user)
            return redirect('admin_dashboard')

        return render(request, 'core/login.html', {
            'error': 'Invalid admin credentials'
        })

    return render(request, 'core/login.html')


# =========================
# 📋 Admin Dashboard
# =========================
@login_required
@user_passes_test(lambda u: u.is_staff)
def admin_dashboard(request):
    pending_students = Student.objects.filter(status='pending')
    verified_students = Student.objects.filter(status='verified')
    rejected_students = Student.objects.filter(status='rejected')

    return render(request, 'core/admin_dashboard.html', {
        'pending_students': pending_students,
        'verified_students': verified_students,
        'rejected_students': rejected_students
    })


# =========================
# ✅ Verify Student + Roll Number
# =========================
@login_required
@user_passes_test(lambda u: u.is_staff)
def verify_student(request, id):
    student = get_object_or_404(Student, id=id)
    student.status = 'verified'

    if not student.roll_number:
        student.roll_number = f"IMS{student.id:04d}"

    student.save()
    return redirect('admin_dashboard')


# =========================
# ❌ Reject Student
# =========================
@login_required
@user_passes_test(lambda u: u.is_staff)
def reject_student(request, id):
    student = get_object_or_404(Student, id=id)
    student.status = 'rejected'
    student.save()
    return redirect('admin_dashboard')


# =========================
# 🗑️ Delete Student (PERMANENT)
# =========================
@login_required
@user_passes_test(lambda u: u.is_staff)
def delete_student(request, id):
    student = get_object_or_404(Student, id=id)

    if request.method == "POST":
        # Delete linked user also
        user = student.user
        student.delete()
        user.delete()

    return redirect('admin_dashboard')


# =========================
# 📋 List All Students (Admin)
# =========================
@login_required
@user_passes_test(lambda u: u.is_staff)
def admin_students(request):
    students = Student.objects.all()
    return render(request, 'core/admin_students.html', {
        'students': students
    })


# =========================
# 🚪 Logout
# =========================
@login_required
def user_logout(request):
    logout(request)
    return redirect('home')
