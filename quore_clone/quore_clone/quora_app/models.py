

from django.db import models
from django.conf import settings

from django.utils import timezone
from common.models import BaseModel


class Question(BaseModel):
    title = models.CharField(max_length=255)
    text = models.TextField()
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        related_name='questions'
    )
 

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']


class Answer(BaseModel):
    text = models.TextField()
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name='answers'
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        related_name='answers'
    )

    def __str__(self):
        author_repr = self.author
        try:
            title = self.question.title[:30] + ('...' if len(self.question.title) > 30 else '')
            return f"Answer to '{title}' by {author_repr}"
        except Question.DoesNotExist:
             return f"Answer by {author_repr} (Question missing)"

    class Meta:
        ordering = ['-created_at']


class Like(BaseModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        related_name='likes'
    )
    answer = models.ForeignKey(
        Answer,
        on_delete=models.CASCADE,
        related_name='likes'
    )

    class Meta:
        unique_together = ('user', 'answer')
        ordering = ['-created_at']

    def __str__(self):
        user_repr = self.user
        try:
            return f"{user_repr} likes answer {self.answer.id}"
        except Answer.DoesNotExist:
             return f"{user_repr} likes (Answer missing)"