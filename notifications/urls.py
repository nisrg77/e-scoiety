from django.urls import path
from . import views

urlpatterns = [
    path('notices/', views.notice_board_view, name='notice_board'),
    path('polls/', views.poll_list_view, name='poll_list'),
    path('polls/vote/', views.vote_view, name='vote'),
]
