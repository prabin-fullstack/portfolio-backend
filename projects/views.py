from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from . models import Project, ProjectSection
from . serializer import ProjectSerializer, ProjectSectionSerializer


class ProjectAPIView(APIView):

    def get(self,request):
        projects = Project.objects.all()
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data)
    
    def post(self,request):
        serializer = ProjectSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(section=ProjectSection.load())
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request,id):
        project = get_object_or_404(Project, id=id)
        serializer = ProjectSerializer(project, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({"message":"Project updated"},status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request,id):
        project = get_object_or_404(Project, id=id)
        project.delete()
        return Response({"message":"Prject deleted successfully "}, status=status.HTTP_204_NO_CONTENT)
        

class ProjectSectionAPIView(APIView):

    def get(self,request):
        section = ProjectSection.load()
        serializer = ProjectSectionSerializer(section)
        return Response(serializer.data)
    
    def put(self, request):
        section = ProjectSection.load()

        serializer = ProjectSectionSerializer(
            section,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
   