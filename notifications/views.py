from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from . import services

@login_required
def notice_board_view(request):
    """
    Shows all society announcements on the digital bulletin board.
    Pinned notices appear first. Admins can also post new notices.
    """
    # Handle admin posting a new notice
    if request.method == 'POST' and request.user.role == 'admin':
        from .models import Notice
        title = request.POST.get('title', '').strip()
        content = request.POST.get('content', '').strip()
        is_pinned = request.POST.get('is_pinned') == 'on'
        if title and content:
            Notice.objects.create(
                title=title,
                content=content,
                created_by=request.user,
                is_pinned=is_pinned
            )
        return redirect('notice_board')
    
    notices = services.get_active_notices()
    
    # Choose the base layout based on the user's role
    if request.user.role == 'admin':
        base_template = 'admin_base.html'
    elif request.user.role == 'security':
        base_template = 'security_base.html'
    else:
        base_template = 'resident_base.html'
    
    context = {
        'notices': notices,
        'base_template': base_template,
        'is_admin': request.user.role == 'admin',
    }
    return render(request, 'notifications/notice_board.html', context)

@login_required
def poll_list_view(request):
    """
    Shows active community polls, allowing residents to cast their voice.
    """
    from .models import Poll
    polls = Poll.objects.filter(is_active=True).order_by('-created_at')
    return render(request, 'notifications/poll_list.html', {'polls': polls})

@login_required
def vote_view(request):
    """
    Handles POST requests when a resident casts a vote on a poll option.
    Delegates the increment logic to the service layer.
    """
    if request.method == 'POST':
        option_id = request.POST.get('option_id')
        services.cast_vote(option_id)
    return redirect('poll_list')
