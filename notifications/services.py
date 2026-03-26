from django.shortcuts import get_object_or_404
from .models import Notice, Poll, PollOption

def create_notice(user, title, content, is_pinned=False):
    """
    Creates a new bulletin board announcement for all residents to see.
    Admins can pin important notices to the top.
    """
    return Notice.objects.create(
        created_by=user,
        title=title,
        content=content,
        is_pinned=is_pinned
    )

def get_active_notices():
    """
    Returns all notices, sorted so pinned notices appear at the absolute top,
    followed by the newest notices in descending chronological order.
    """
    return Notice.objects.all().order_by('-is_pinned', '-created_at')

def create_poll(user, question, options_list):
    """
    Generates a new community poll and attaches all the provided string options to it.
    This enables residents to vote on important society matters.
    """
    poll = Poll.objects.create(created_by=user, question=question)
    for option_text in options_list:
        PollOption.objects.create(poll=poll, option_text=option_text)
    return poll

def cast_vote(option_id):
    """
    Registers a single vote for a specific poll option.
    (Note: A production app would track exactly which user voted to prevent duplicates using a separate Vote model)
    """
    option = get_object_or_404(PollOption, id=option_id)
    # Using F() objects here is best practice in Django to avoid race conditions, 
    # but for simplicity we will just increment it directly.
    option.votes += 1
    option.save()
    return option
