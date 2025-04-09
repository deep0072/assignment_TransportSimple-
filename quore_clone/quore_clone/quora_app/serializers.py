from rest_framework import serializers
from accounts.serializers import UserSerializer
from .models import Question,Answer,Like



class LikeSerializer(serializers.ModelSerializer):
    """ Serializer for the Like model """

    user = UserSerializer(read_only=True)

    class Meta:
        model = Like
        fields = ['id', 'user', 'answer', 'created_at']
     
        read_only_fields = ['user', 'created_at']

class QuestionSerializer(serializers.ModelSerializer):
    """ Serializer for the Question model """
   
    author = UserSerializer(read_only=True)
   
    answers_count = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Question
        fields = [
            'id', 'title', 'text', 'author', 'created_at', 'updated_at',
            'answers_count'
        ]
        
        read_only_fields = ['author', 'created_at', 'updated_at', 'answers_count']

    def get_answers_count(self, obj):
        """ Calculate the total number of answers for the question """
     
        return obj.answers.count()
class AnswerSerializer(serializers.ModelSerializer):
    """ Serializer for the Answer model """

    author = UserSerializer(read_only=True)
    
   
    likes_count = serializers.SerializerMethodField(read_only=True)
    is_liked_by_current_user = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Answer
        fields = [
            'id', 'text', 'author', 'created_at', 'updated_at',
            'likes_count', 'is_liked_by_current_user'
        ]
       
        read_only_fields = ['author', 'created_at', 'updated_at',
                          'likes_count', 'is_liked_by_current_user']

    def get_likes_count(self, obj):
        """ Calculate the total number of likes for the answer """
       
        return obj.likes.count()

    def get_is_liked_by_current_user(self, obj):
        """ Check if the current request's user has liked this answer """
        user = self.context['request'].user
        if user and user.is_authenticated:
         
            return Like.objects.filter(answer=obj, user=user).exists()
        return False

