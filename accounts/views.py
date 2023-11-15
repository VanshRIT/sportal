# accounts/views.py
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from accounts.forms import CustomLoginForm

class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'  # Create this template
    authentication_form = CustomLoginForm

    def form_valid(self, form):
        user = form.get_user()
        if user.user_type == 'Teacher':
            return redirect('teacher_dashboard')  # Define the URL name for the teacher dashboard
        elif user.user_type == 'Parent':
            return redirect('parent_dashboard')  # Define the URL name for the parent dashboard
        elif user.user_type == 'Counselor':
            return redirect('counselor_dashboard')  # Define the URL name for the counselor dashboard
        elif user.user_type == 'IT Admin':
            return redirect('itadmin_dashboard')  # Define the URL name for the IT admin dashboard
        else:
            return redirect('login')  # Redirect to login page if user_type is not recognized
