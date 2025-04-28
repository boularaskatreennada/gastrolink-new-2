from django.http import HttpResponseForbidden
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from functools import wraps

def pdg_required(view_func):
    @wraps(view_func)
    @login_required
    def _wrapped_view(request, *args, **kwargs):
        if request.user.user_type != 'PDG':
            return HttpResponseForbidden("You are not allowed here.")
        return view_func(request, *args, **kwargs)
    return _wrapped_view

def manager_required(view_func):
    @wraps(view_func)
    @login_required
    def _wrapped_view(request, *args, **kwargs):
        if request.user.user_type != 'MANAGER':
            return HttpResponseForbidden("You are not allowed here.")
        return view_func(request, *args, **kwargs)
    return _wrapped_view


def chef_required(view_func):
    @wraps(view_func)
    @login_required
    def _wrapped_view(request, *args, **kwargs):
        if request.user.user_type != 'CHEF':
            return HttpResponseForbidden("You are not allowed here.")
        return view_func(request, *args, **kwargs)
    return _wrapped_view
    
def waiter_required(view_func):
    @wraps(view_func)
    @login_required
    def _wrapped_view(request, *args, **kwargs):
        if request.user.user_type != 'WAITER':
            return HttpResponseForbidden("You are not allowed here.")
        return view_func(request, *args, **kwargs)
    return _wrapped_view


def delivery_required(view_func):
    @wraps(view_func)
    @login_required
    def _wrapped_view(request, *args, **kwargs):
        if request.user.user_type != 'DELIVERY':
            return HttpResponseForbidden("You are not allowed here.")
        return view_func(request, *args, **kwargs)
    return _wrapped_view

def client_required(view_func):
    @wraps(view_func)
    @login_required
    def _wrapped_view(request, *args, **kwargs):
        if request.user.user_type != 'CLIENT':
            return HttpResponseForbidden("You are not allowed here.")
        return view_func(request, *args, **kwargs)
    return _wrapped_view

def all_roles_required(view_func):
    @wraps(view_func)
    @login_required
    def _wrapped_view(request, *args, **kwargs):
        if request.user.user_type not in ['PDG', 'MANAGER', 'CHEF', 'WAITER', 'CLIENT']:
            return HttpResponseForbidden("You are not allowed here.")
        return view_func(request, *args, **kwargs)
    return _wrapped_view

