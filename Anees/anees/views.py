import datetime
from django.shortcuts import get_object_or_404

import requests
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle
from rest_framework.views import APIView

from .models import Child, ChildLevel, Level
from .serializers import (
    ChildSerializer,
    ChildUpdateSerializer,
    ExpressiveSerializer,
    LevelDetailSerializer,
    LevelSerializer,
    ReceptiveSerializer,
    SimpleExpressiveSerializer,
    SimpleSocialSerializer,
    SocialSerializer,
)
from django.contrib.auth import get_user_model


User = get_user_model()


class ChildrenListApiView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        children = Child.objects.all().prefetch_related("levels").select_related("user")
        serializer = ChildSerializer(children, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ChildDetailApiView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        child = request.user.child
        serializer = ChildSerializer(child)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request):
        child = request.user.child
        serializer = ChildUpdateSerializer(child, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChildrenProfilesApiView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        user = request.user
        if not user.is_staff and user.id != pk:
            return Response(
                {"error": "You Are Not Allowed To Access This Profile"},
                status=status.HTTP_403_FORBIDDEN,
            )
        else:
            user = get_object_or_404(User.objects.select_related("child").filter(pk=pk))

            serializer = ChildSerializer(user.child)
            return Response(serializer.data, status=status.HTTP_200_OK)


class ChildrenProfilesWordsApiView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        user = request.user
        if not user.is_staff and user.id != pk:
            return Response(
                {"error": "You Are Not Allowed To Access These Data"},
                status=status.HTTP_403_FORBIDDEN,
            )
        else:
            user = get_object_or_404(User.objects.select_related("child").filter(pk=pk))
            child = user.child
            receptive_words = []
        expressive_words = []
        for level in child.levels.all().select_related("level__receptive"):
            if level.receptive_complete:
                try:
                    if level.level.receptive.answer:
                        receptive_words.append(level.level.receptive.answer)
                except:
                    pass

        for level in child.levels.all().select_related("level__expressive"):
            if level.expressive_complete:
                try:
                    if level.level.expressive.answer:
                        expressive_words.append(level.level.expressive.answer)
                except:
                    pass

        words = {"receptive": receptive_words, "expressive": expressive_words}
        return Response({"words": words}, status=status.HTTP_200_OK)


class ChildWordsApiView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        child = request.user.child
        receptive_words = []
        expressive_words = []
        for level in child.levels.all().select_related("level__receptive"):
            if level.receptive_complete:
                try:
                    if level.level.receptive.answer:
                        receptive_words.append(level.level.receptive.answer)
                except:
                    pass

        for level in child.levels.all().select_related("level__expressive"):
            if level.expressive_complete:
                try:
                    if level.level.expressive.answer:
                        expressive_words.append(level.level.expressive.answer)
                except:
                    pass

        words = {"receptive": receptive_words, "expressive": expressive_words}
        return Response({"words": words}, status=status.HTTP_200_OK)


class LevelListApiView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        child = request.user.child
        levels = child.levels.select_related("level").all()
        serializer = LevelSerializer(levels, many=True, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class LevelDetailApiView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        child = request.user.child
        level = child.levels.select_related("level").filter(level__level_num=pk).first()
        if not level:
            if request.user.is_staff:
                return Response(
                    {"error": "Level Does Not Exist"},
                    status=status.HTTP_404_NOT_FOUND,
                )
            else:
                return Response(
                    {"error": "You Are Not Allowed To Access This Level"},
                    status=status.HTTP_401_UNAUTHORIZED,
                )
        serializer = LevelDetailSerializer(level, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class ReceptiveApiView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        child = request.user.child
        try:
            level = (
                child.levels.select_related("level__receptive")
                .prefetch_related("level__receptive__images")
                .filter(level__level_num=pk)
                .first()
            )
        except Exception as e:
            return Response(
                {"error": "The Game You Are Looking For Does Not Exist"},
                status=status.HTTP_404_NOT_FOUND,
            )
        if not level:
            return Response(
                {"error": "You Are Not Allowed To Access This Level"},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        try:
            serializer = ReceptiveSerializer(level.level.receptive)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"error": "The Game You Are Looking For Does Not Exist"},
                status=status.HTTP_404_NOT_FOUND,
            )

    def post(self, request, pk):
        child = request.user.child
        level = (
            child.levels.select_related("level__receptive")
            .prefetch_related("level__receptive__images")
            .filter(level__level_num=pk)
            .first()
        )
        new_high_score = False
        if not level:
            return Response(
                {"error": "You Are Not Allowed To Access This Level"},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        game = None
        try:
            game = level.level.receptive
        except Exception as e:
            return Response(
                {"error": "The Game You Are Looking For Does Not Exist"},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = ReceptiveSerializer(game, data=request.data)
        if serializer.is_valid():
            level.receptive_complete = True

            if level.receptive_score < serializer.validated_data["score"]:
                level.receptive_score = serializer.validated_data["score"]
                new_high_score = True
            level.save()
            if level.expressive_complete and level.social_complete:
                if not level.completed_date:
                    level.completed_date = datetime.date.today()
                current_level = level.level.level_num
                next_level = Level.objects.filter(level_num=current_level + 1).first()
                if next_level:
                    if not child.levels.filter(level=next_level).exists():
                        newChildLevel = ChildLevel.objects.create(
                            child=child, level=next_level
                        )

                        newChildLevel.save()
                        return Response(
                            {"success": "You Have Passed This Level"},
                            status=status.HTTP_200_OK,
                        )

                    if new_high_score:
                        return Response(
                            {
                                "success": "You Have Passed This Level With New High Score"
                            },
                            status=status.HTTP_200_OK,
                        )
                    else:
                        return Response(
                            {"success": "You Have Passed This Level"},
                            status=status.HTTP_200_OK,
                        )
                else:
                    return Response(
                        {"success": "You Have Finished All Levels"},
                        status=status.HTTP_200_OK,
                    )

            return Response(
                {"success": "You Have Completed This Game"}, status=status.HTTP_200_OK
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ExpressiveApiView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        child = request.user.child
        level = (
            child.levels.select_related("level__expressive")
            .filter(level__level_num=pk)
            .first()
        )

        if not level:
            return Response(
                {"error": "You Are Not Allowed To Access This Level"},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        try:
            serializer = ExpressiveSerializer(level.level.expressive)
            return Response(serializer.data)
        except Exception as e:
            return Response(
                {"error": "The Game You Are Looking For Does Not Exist"},
                status=status.HTTP_404_NOT_FOUND,
            )

    def post(self, request, pk):
        child = request.user.child
        level = (
            child.levels.select_related("level__expressive")
            .filter(level__level_num=pk)
            .first()
        )
        new_high_score = False
        if not level:
            return Response(
                {"error": "You Are Not Allowed To Access This Level"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        game = None
        try:
            game = level.level.expressive
        except Exception as e:
            return Response(
                {"error": "The Game You Are Looking For Does Not Exist"},
                status=status.HTTP_404_NOT_FOUND,
            )
        serializer = SimpleExpressiveSerializer(game, data=request.data)
        if serializer.is_valid():
            level.expressive_complete = True
            if level.expressive_score < serializer.validated_data["score"]:
                level.expressive_score = serializer.validated_data["score"]
                new_high_score = True
            level.save()
            if level.receptive_complete and level.social_complete:
                if not level.completed_date:
                    level.completed_date = datetime.date.today()
                current_level = level.level.level_num
                next_level = Level.objects.filter(level_num=current_level + 1).first()
                if next_level:
                    if not child.levels.filter(level=next_level).exists():
                        newChildLevel = ChildLevel.objects.create(
                            child=child, level=next_level
                        )
                        newChildLevel.save()
                        return Response(
                            {"success": "You Have Passed This Level"},
                            status=status.HTTP_200_OK,
                        )

                    if new_high_score:
                        return Response(
                            {
                                "success": "You Have Passed This Level With New High Score"
                            },
                            status=status.HTTP_200_OK,
                        )
                    else:
                        return Response(
                            {"success": "You Have Passed This Level"},
                            status=status.HTTP_200_OK,
                        )
                else:
                    return Response(
                        {"success": "You Have Finished All Levels"},
                        status=status.HTTP_200_OK,
                    )

            return Response(
                {"success": "You Have Completed This Game"}, status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SocialApiView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        child = request.user.child
        level = (
            child.levels.select_related("level__social")
            .prefetch_related("level__social__messages")
            .filter(level__level_num=pk)
            .first()
        )
        if not level:
            return Response(
                {"error": "You Are Not Allowed To Access This Level"},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        try:
            serializer = SocialSerializer(level.level.social)
            return Response(serializer.data)
        except Exception as e:
            return Response(
                {"error": "The Game You Are Looking For Does Not Exist"},
                status=status.HTTP_404_NOT_FOUND,
            )

    def post(self, request, pk):
        child = request.user.child
        level = (
            child.levels.select_related("level__social")
            .prefetch_related("level__social__messages")
            .filter(level__level_num=pk)
            .first()
        )
        new_high_score = False
        if not level:
            return Response(
                {"error": "You Are Not Allowed To Access This Level"},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        game = None
        try:
            game = level.level.social
        except Exception as e:
            return Response(
                {"error": "The Game You Are Looking For Does Not Exist"},
                status=status.HTTP_404_NOT_FOUND,
            )
        serializer = SimpleSocialSerializer(game, data=request.data)
        if serializer.is_valid():
            level.social_complete = True
            if level.social_score < serializer.validated_data["score"]:
                level.social_score = serializer.validated_data["score"]
                new_high_score = True
            level.save()
            if level.expressive_complete and level.receptive_complete:
                if not level.completed_date:
                    level.completed_date = datetime.date.today()
                    level.save()
                current_level = level.level.level_num
                next_level = Level.objects.filter(level_num=current_level + 1).first()
                if next_level:
                    if not child.levels.filter(level=next_level).exists():
                        newChildLevel = ChildLevel.objects.create(
                            child=child, level=next_level
                        )
                        newChildLevel.save()
                        return Response(
                            {"success": "You Have Passed This Level"},
                            status=status.HTTP_200_OK,
                        )
                    if new_high_score:
                        return Response(
                            {
                                "success": "You Have Passed This Level With New High Score"
                            },
                            status=status.HTTP_200_OK,
                        )
                    else:
                        return Response(
                            {"success": "You Have Passed This Level"},
                            status=status.HTTP_200_OK,
                        )
                else:
                    return Response(
                        {"success": "You Have Finished All Levels"},
                        status=status.HTTP_200_OK,
                    )

            return Response(
                {"success": "You Have Completed This Game"}, status=status.HTTP_200_OK
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AIModelApiView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data
        label = data.get("label")
        if not label:
            return Response(
                {"error": "Please Provide A Label"}, status=status.HTTP_400_BAD_REQUEST
            )
        if not data.get("file"):
            return Response(
                {"error": "Please Provide A File"}, status=status.HTTP_400_BAD_REQUEST
            )
        uploadedFile = request.FILES["file"]

        response = requests.post(
            f"http://54.86.189.155:8000/predict?label={label}&access_token=eyJhbGciOiJIUzI1NiJ9.eyJSb2xlIjoiQWRtaW4iLCJVc2VybmFtZSI6IkphdmFJblVzZSIsImFuZWVzIjoiSXNzdWVyIiwiZXhwIjoxNjg2MzQ3ODM1LCJpYXQiOjE2ODYzNDc4MzV9.0svsjbKCsx-cPElCF4EOvHh6KkfFYxhjBEjbBAjkbHE",
            files={"file": uploadedFile},
        )

        return Response(response.json(), status=response.status_code)
