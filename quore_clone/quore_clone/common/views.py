from django.shortcuts import render
from rest_framework.views import APIView
# Create your views here.
from rest_framework.permissions import IsAuthenticated


class BaseView(APIView):
    permission_classes = [IsAuthenticated]