from rest_framework import generics
from django.shortcuts import render

from users.models import User


class UserAPIView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = WomenSerializer
