from rest_framework.reverse import reverse
from rest_framework import serializers
from . import models
from core.serializers import UserCreateSerializer
from django.utils import timezone


class ChildSerializer(serializers.ModelSerializer):
    user_info = UserCreateSerializer(source="user", read_only=True)
    accuracy = serializers.SerializerMethodField(read_only=True)
    current_level = serializers.SerializerMethodField(read_only=True)
    join_duration_in_days = serializers.SerializerMethodField(read_only=True)
    words = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = models.Child
        fields = [
            "picture",
            "current_level",
            "join_duration_in_days",
            "accuracy",
            "words",
            "user_info",
        ]

    def get_current_level(self, child: models.Child):
        return child.levels.all().count()

    def get_join_duration_in_days(self, child: models.Child):
        now = timezone.now()
        return (now - child.date_joined).days

    def get_accuracy(self, child: models.Child):
        levels = child.levels.all().select_related("level")
        receptive_score = 0
        expressive_score = 0
        social_score = 0
        receptive_count = 0
        expressive_count = 0
        social_count = 0
        for level in levels:
            if level.completed:
                receptive_score += level.receptive_score
                receptive_count += 1
                expressive_score += level.expressive_score
                expressive_count += 1
                social_score += level.social_score
                social_count += 1
        receptive_score = (
            0 if receptive_count == 0 else receptive_score / receptive_count
        )
        expressive_score = (
            0 if expressive_count == 0 else expressive_score / expressive_count
        )
        social_score = 0 if social_count == 0 else social_score / social_count

        return {
            "receptive": receptive_score,
            "expressive": expressive_score,
            "social": social_score,
        }

    def get_words(self, child: models.Child):
        return reverse("child-words", request=self.context.get("request"))


class ChildUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Child
        fields = ["picture"]


class LevelSerializer(serializers.ModelSerializer):
    level_num = serializers.SerializerMethodField()
    level = serializers.SerializerMethodField()

    class Meta:
        model = models.ChildLevel
        fields = ["level_num", "level"]

    def get_level(self, childlevel: models.ChildLevel):
        request = self.context.get("request")
        return reverse(
            "level-detail", kwargs={"pk": childlevel.level.level_num}, request=request
        )

    def get_level_num(self, level: models.ChildLevel):
        return level.level.level_num


class LevelDetailSerializer(serializers.ModelSerializer):
    level_num = serializers.SerializerMethodField()
    score = serializers.SerializerMethodField()

    receptive = serializers.SerializerMethodField()
    expressive = serializers.SerializerMethodField()
    social = serializers.SerializerMethodField()

    class Meta:
        model = models.ChildLevel
        fields = [
            "level_num",
            "receptive",
            "expressive",
            "social",
            "completed_date",
            "joined_date",
            "receptive_score",
            "receptive_complete",
            "expressive_score",
            "expressive_complete",
            "social_complete",
            "social_score",
            "score",
        ]

    def get_receptive(self, childlevel: models.ChildLevel):
        request = self.context.get("request")
        try:
            if childlevel.level.receptive:
                return reverse(
                    "receptive",
                    kwargs={"pk": childlevel.level.level_num},
                    request=request,
                )
        except Exception as e:
            return None

    def get_expressive(self, childlevel: models.ChildLevel):
        request = self.context.get("request")
        try:
            if childlevel.level.expressive:
                return reverse(
                    "expressive",
                    kwargs={"pk": childlevel.level.level_num},
                    request=request,
                )
        except Exception as e:
            return None

    def get_social(self, childlevel: models.ChildLevel):
        request = self.context.get("request")
        try:
            if childlevel.level.social:
                return reverse(
                    "social",
                    kwargs={"pk": childlevel.level.level_num},
                    request=request,
                )
        except:
            return None

    def get_level_num(self, level: models.ChildLevel):
        return level.level.level_num

    def get_score(self, childlevel: models.ChildLevel):
        total = (
            childlevel.receptive_score
            + childlevel.expressive_score
            + childlevel.social_score
        )
        return total / 3 if total else 0


class ReceptiveImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ReceptiveImage
        fields = ["id", "img", "name"]


class ReceptiveSerializer(serializers.ModelSerializer):
    images = ReceptiveImageSerializer(many=True, read_only=True)
    score = serializers.IntegerField(write_only=True)
    answer = serializers.CharField(read_only=True)

    class Meta:
        model = models.Receptive
        fields = ["id", "answer", "images", "score"]


class ExpressiveSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Expressive
        fields = ["id", "img", "answer"]


class SimpleExpressiveSerializer(serializers.ModelSerializer):
    score = serializers.IntegerField(write_only=True)

    class Meta:
        model = models.Expressive
        fields = ["score"]


class SocialMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.conversionMessage
        fields = ["id", "message"]


class SocialSerializer(serializers.ModelSerializer):
    messages = SocialMessageSerializer(many=True, read_only=True)
    score = serializers.IntegerField(write_only=True)

    class Meta:
        model = models.Social
        fields = ["id", "video", "messages", "score"]


class SimpleSocialSerializer(serializers.ModelSerializer):
    score = serializers.IntegerField(write_only=True)

    class Meta:
        model = models.Social
        fields = ["score"]
