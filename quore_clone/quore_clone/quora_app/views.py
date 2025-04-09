from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status,pagination

from .serializers import *
from rest_framework import  permissions, status
from django.shortcuts import get_object_or_404
from .paginations import CustomPagination

class QuestionListCreateView(APIView):
    """
    GET: List all questions (ordered by creation date).
    POST: Create a new question (requires authentication).
    """
    serializer_class = QuestionSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    pagination_class =  CustomPagination

    def get(self, request):
        """ Handle listing all questions """
        questions = Question.objects.all().select_related('author').order_by('-created_at')

        paginator = self.pagination_class()
        paginated_questions = paginator.paginate_queryset(questions, request)
        serializer = self.serializer_class(paginated_questions, many=True, context={'request': request})
        return paginator.get_paginated_response(serializer.data)

    def post(self, request, *args, **kwargs):
        """ Handle creating a question """
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
          
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class QuestionDetailView(APIView):
    """
    GET: Retrieve details of a specific question by its ID.
    (Could be extended to RetrieveUpdateDestroyAPIView if edit/delete is needed)
    """
    serializer_class = QuestionSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request, *args, **kwargs):
        """ Handle retrieving a single question """
        question = get_object_or_404(Question.objects.select_related('author'), pk=self.kwargs.get('pk'))
        serializer = self.serializer_class(question, context={'request': request})
        return Response(serializer.data)

  




class AnswerListCreateView(APIView):
    """
    GET: List answers for a specific question (identified by question_pk in URL).
    POST: Create a new answer for that question (requires authentication).
    """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = AnswerSerializer
    pagination_class = CustomPagination

    def get(self, request, *args, **kwargs):
        """ Handle listing answers for a question """
        question_id = self.kwargs.get('question_pk')
        get_object_or_404(Question, pk=question_id)

        """ Filter answers based on the question_pk from the URL """
        answers = Answer.objects.filter(question_id=question_id) .select_related('author').prefetch_related('likes').order_by('-created_at')
        paginator = self.pagination_class()
        paginated_answers = paginator.paginate_queryset(answers, request)
        serializer = self.serializer_class(paginated_answers, many=True, context={'request': request})
        return paginator.get_paginated_response(serializer.data)


    def post(self, request,**kwargs):
        """ Handle creating an answer """
        question_id = self.kwargs.get('question_pk')
        question = get_object_or_404(Question, pk=question_id)
        
        serializer = self.serializer_class(data=request.data, context={'request': request})
        if serializer.is_valid(raise_exception=True):      
            serializer.save(author=request.user, question=question)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)










# --- Like Views ---

class LikeToggleView(APIView):
    """
    POST: Like an answer (if not already liked).
    DELETE: Unlike an answer (if liked). 
    Requires authentication.
    Identifies the answer by answer_pk in the URL.
    """
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request, *args, **kwargs):
        """ Handle Liking an answer """
        answer_id = self.kwargs.get('answer_pk')
        question_obj = get_object_or_404(Question, pk=request.data.pop('question_id')) 

        answer = get_object_or_404(Answer, pk=answer_id,question=question_obj) 
        user = request.user 

       
        like, created = Like.objects.get_or_create(user=user, answer=answer) 

        if created:

            serializer = LikeSerializer(like, context={'request': request}) 
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            like.delete()
            return Response({"message":"disliked succesfully"},status=status.HTTP_204_NO_CONTENT)
            

    def get(self, request, *args, **kwargs):
        """ Handle retrieving likes for an answer """
        answer_id = self.kwargs.get('answer_pk')
        answer = get_object_or_404(Answer, pk=answer_id)
        likes = Like.objects.filter(answer=answer,)
        serializer = LikeSerializer(likes, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    