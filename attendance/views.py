from django.shortcuts import render
from .models import Attendance

def view_attendance(request):
    attendances = Attendance.objects.all()
    return render(request, 'attendance/view_attendance.html', {'attendances': attendances})

def add_attendance(request):
    if request.method == 'POST':
        # Handle form submission and create a new attendance record
    else:
        # Display the attendance form for input
        return render(request, 'attendance/add_attendance.html')
