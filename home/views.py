from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from .models import HeroContent, AboutContent, Stat, Messages
from .serializers import HeroContentSerializer, AboutContentSerializer, StatSerializer , MessageSerializer


class HeroContentAPIView(APIView):

    def get_object(self):
        return HeroContent.load()

    def get(self, request):
        hero = self.get_object()
        serializer = HeroContentSerializer(hero)
        return Response(serializer.data)

    def put(self, request):
        hero = self.get_object()
        serializer = HeroContentSerializer(hero, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request):
        hero = self.get_object()
        serializer = HeroContentSerializer(hero, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AboutContentAPIView(APIView):

    def get_object(self):
        return AboutContent.load()

    def get(self, request):
        about = self.get_object()
        serializer = AboutContentSerializer(about)
        return Response(serializer.data)

    def put(self, request):
        about = self.get_object()
        serializer = AboutContentSerializer(about, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request):
        about = self.get_object()
        serializer = AboutContentSerializer(about, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class StatListCreateAPIView(generics.ListCreateAPIView):
    queryset = Stat.objects.all()
    serializer_class = StatSerializer


class StatRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Stat.objects.all()
    serializer_class = StatSerializer


class MessagesAPIView(APIView):
    def get(self,request):
        messages = Messages.objects.all()
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = MessageSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
    
    def patch(self,request,id):
        message = get_object_or_404(Messages, id=id)
        serializer = MessageSerializer(
        message,
        data=request.data,
        partial=True
    )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def delete(self,request,id):
        message = get_object_or_404(Messages, id=id)
        message.delete()
        return Response({"message":"Message Deleted successfully"},status=status.HTTP_204_NO_CONTENT)
    
class LogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(
                {"message": "Logged out successfully"},
                status=status.HTTP_205_RESET_CONTENT,
            )

        except Exception:
            return Response(
                {"error": "Invalid refresh token"},
                status=status.HTTP_400_BAD_REQUEST,
            )