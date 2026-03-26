from django.db import models
from django.conf import settings

class Notice(models.Model):
    """
    Bulletin board announcements created by admins for the society.
    """
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notices')
    created_at = models.DateTimeField(auto_now_add=True)
    is_pinned = models.BooleanField(default=False)

    def __str__(self):
        return self.title

class Poll(models.Model):
    """
    A voting mechanism for community decisions.
    """
    question = models.CharField(max_length=255)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='polls')
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.question

class PollOption(models.Model):
    """
    Individual answers for a specific Poll.
    """
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name='options')
    option_text = models.CharField(max_length=255)
    votes = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.option_text} ({self.votes} votes)"
