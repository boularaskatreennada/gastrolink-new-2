from django.shortcuts import redirect
from django.urls import reverse

class RoleBasedAccessMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Code that runs on every request BEFORE the view
        response = self.get_response(request)
        # Code that runs on every request AFTER the view
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        # Skip middleware for login page and admin
        if request.path.startswith('/admin/') or request.path.startswith('/login/'):
            return None
        
        # If not authenticated, redirect to login
        if not request.user.is_authenticated:
            return redirect(reverse('login'))
        
        # Check user types for specific paths
        user_type = request.user.user_type
        
        if '/pdg-dashboard/' in request.path and user_type != 'PDG':
            return redirect(reverse('login'))
        elif '/manager-dashboard/' in request.path and user_type != 'MANAGER':
            return redirect(reverse('login'))
        # Add checks for other dashboard paths
        
        return None