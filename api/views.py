from django.shortcuts import render

from api.serializers import UserSerializer,ProfileSerializer,QuestionSerializer,AnswerSerializer,serializers
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet,ModelViewSet,GenericViewSet
from rest_framework.mixins import CreateModelMixin
from rest_framework.generics import GenericAPIView
from stack.models import UserProfile,Questions,Answers
from rest_framework import authentication,permissions
from rest_framework.decorators import action


# class UsersView(ViewSet):
#     serializer_class=UserSerializer

#     def create(self,request,*args,**kwargs):
#         serializer=UserSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(data=serializer.data)
#         else:
#             return Response(data=serializer.errors)

class UsersView(GenericViewSet,CreateModelMixin):
    serializer_class=UserSerializer
    queryset=User.objects.all()

class ProfileView(ModelViewSet):
    serializer_class=ProfileSerializer
    queryset=UserProfile.objects.all()
    # authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


    # def get_queryset(self):
    #     return UserProfile.objects.filter(user=self.request.user)
    

    def destroy(self,request,*args,**kwargs):
        prof=self.get_object()
        if prof.user !=request.user:
            raise serializers.ValidationError("not allowed to perform")
        else:
            print("deleted")
            return super().destroy(request,*args,**kwargs)

    # def list(self, request, *args, **kwargs):
    #     qs=UserProfile.objects.get(user=request.user)
    #     serializer=ProfileSerializer(qs,many=False)
    #     return Response(data=serializer.data)

    # def create(self,request,*args,**kwargs):
    #     serializer=ProfileSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save(user=request.user)
    #         return Response(data=serializer.data)
    #     else:
    #         return Response(data=serializer.errors)

class QuestionsView(ModelViewSet):
    serializer_class=QuestionSerializer
    queryset=Questions.objects.all()
    # authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    # def get_queryset(self):
    #     return Questions.objects.all().order_by("-created_date")

    @action(methods=["post"],detail=True)
    def add_answer(self,request,*args,**kwargs):
        serializer=AnswerSerializer(data=request.data)
        id=kwargs.get("pk")
        quest=Questions.objects.get(id=id)
        # quest=self.get_object()         (also correct)
        user=request.user
        if serializer.is_valid():
            serializer.save(question=quest,user=user)
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)
        
class AnswersView(ModelViewSet):
    serializer_class=AnswerSerializer
    queryset=Answers.objects.all()
    # authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        raise serializers.ValidationError("Method Not Allowed !!!")
    
    @action(methods=["post"],detail=True)
    def add_upvote(self,request,*args,**kwargs):
        answer=self.get_object()
        answer.up_vote.add(request.user)
        answer.save()
        return Response(data="UpVoted.")
    
    @action(methods=["post"],detail=True)
    def down_upvote(self,request,*args,**kwargs):
        answer=self.get_object()
        answer.up_vote.remove(request.user)
        answer.save()
        return Response(data="UpVote Removed..")
    
