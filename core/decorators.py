from django.contrib.auth.decorators import user_passes_test

def is_admin(user):
    return user.is_authenticated and getattr(user, 'role', None) == 'admin'

def is_resident(user):
    return user.is_authenticated and getattr(user, 'role', None) == 'resident'

def is_security(user):
    return user.is_authenticated and getattr(user, 'role', None) == 'security'

def admin_required(function=None, redirect_field_name='next', login_url='login'):
    """
    Decorator for views that checks that the user is logged in and is an admin,
    redirecting to the login page if necessary.
    """
    actual_decorator = user_passes_test(
        is_admin,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator

def resident_required(function=None, redirect_field_name='next', login_url='login'):
    """
    Decorator for views that checks that the user is logged in and is a resident,
    redirecting to the login page if necessary.
    """
    actual_decorator = user_passes_test(
        is_resident,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator

def security_required(function=None, redirect_field_name='next', login_url='login'):
    """
    Decorator for views that checks that the user is logged in and is a security guard,
    redirecting to the login page if necessary.
    """
    actual_decorator = user_passes_test(
        is_security,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator
