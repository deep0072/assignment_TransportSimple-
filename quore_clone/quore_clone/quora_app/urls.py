from django.contrib import admin
from django.urls import path
from .views import *


urlpatterns = [
    
    path('questions/', QuestionListCreateView.as_view(), name='question-list-create'),
    path('questions/<int:pk>/', QuestionDetailView.as_view(), name='question-detail'),
    path('questions/<int:question_pk>/answers/', AnswerListCreateView.as_view(), name='answer-list-create'),
    path('answers/<int:answer_pk>/like/', LikeToggleView.as_view(), name='answer-like'),
]
