from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from .models import SkillsSection, SkillGroup, Skill
from .serializers import (
    SkillsSectionSerializer,
    SkillGroupSerializer,
    SkillSerializer,
)

# Create your views here.

class SkillsSectionAPIView(APIView):

    def get(self, request):
        section = SkillsSection.load()
        serializer = SkillsSectionSerializer(section)
        return Response(serializer.data)

    def put(self, request):
        section = SkillsSection.load()

        serializer = SkillsSectionSerializer(
            section,
            data=request.data
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)