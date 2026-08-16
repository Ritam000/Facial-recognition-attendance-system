from .forms import StudentForm
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from .models import Student

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('student_list')  # we'll create this page next
        else:
            return render(request, 'admin_panel/login.html', {'error': 'Invalid username or password'})
    return render(request, 'admin_panel/login.html')

from django.contrib.auth.decorators import login_required



@login_required(login_url='login')
def student_list(request):
    students = Student.objects.all()
    return render(request, 'admin_panel/student_list.html', {'students': students})



@login_required(login_url='login')
def register_student(request):
    if request.method == 'POST':
        form = StudentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('student_list')
    else:
        form = StudentForm()
    return render(request, 'admin_panel/register.html', {'form': form})


from django.shortcuts import get_object_or_404

@login_required(login_url='login')
def edit_student(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    if request.method == 'POST':
        form = StudentForm(request.POST, request.FILES, instance=student)
        if form.is_valid():
            form.save()
            return redirect('student_list')
    else:
        form = StudentForm(instance=student)
    return render(request, 'admin_panel/edit_student.html', {'form': form, 'student': student})



@login_required(login_url='login')
def delete_student(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    student.delete()
    return redirect('student_list')