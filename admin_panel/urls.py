from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('students/', views.student_list, name='student_list'),
    path('register/', views.register_student, name='register_student'),
     path('edit/<int:student_id>/', views.edit_student, name='edit_student'),
    path('delete/<int:student_id>/', views.delete_student, name='delete_student'),
]