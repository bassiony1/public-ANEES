from django.db import models
from datetime import date
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()


class Child(models.Model):
    picture = models.ImageField(upload_to="profile/images", null=True, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    date_joined = models.DateTimeField(default=timezone.now)

    # levels
    class Meta:
        verbose_name_plural = "Children"
        ordering = ["user__first_name", "user__last_name"]

    @property
    def age(self):
        today = date.today()
        age = (
            today.year
            - self.user.date_of_birth.year
            - (
                (today.month, today.day)
                < (self.user.date_of_birth.month, self.user.date_of_birth.day)
            )
        )
        return age

    @property
    def full_name(self):
        return self.user.get_full_name()

    @property
    def gender(self):
        return self.user.gender

    def __str__(self):
        return self.full_name


class Level(models.Model):
    level_num = models.IntegerField(unique=True)
    # receptive
    # expressive
    # social
    # children

    def __str__(self) -> str:
        return f"Level {self.level_num}"

    class Meta:
        ordering = ["level_num"]


class ChildLevel(models.Model):
    child = models.ForeignKey(Child, on_delete=models.CASCADE, related_name="levels")
    level = models.ForeignKey(Level, on_delete=models.CASCADE, related_name="children")
    receptive_complete = models.BooleanField(default=False)
    expressive_complete = models.BooleanField(default=False)
    social_complete = models.BooleanField(default=False)
    receptive_score = models.SmallIntegerField(default=0)
    expressive_score = models.SmallIntegerField(default=0)
    social_score = models.SmallIntegerField(default=0)
    joined_date = models.DateField(auto_now_add=True)
    completed_date = models.DateField(null=True, blank=True)

    @property
    def completed(self):
        return (
            self.receptive_complete
            and self.expressive_complete
            and self.social_complete
        )

    def __str__(self) -> str:
        return f"{self.child.full_name} - {self.level}"

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["level", "child"], name="level_child_key")
        ]
        ordering = ["level"]
        verbose_name_plural = "Children Progress"


class Receptive(models.Model):
    answer = models.CharField(max_length=255)
    level = models.OneToOneField(Level, on_delete=models.CASCADE)

    # images
    class Meta:
        verbose_name_plural = "Receptive Games"
        ordering = ["level"]

    def __str__(self) -> str:
        return f"{self.level}'s Receptive Game"


class ReceptiveImage(models.Model):
    img = models.ImageField(upload_to="level/receptive")
    name = models.CharField(max_length=255)
    receptive = models.ForeignKey(
        Receptive, on_delete=models.CASCADE, related_name="images"
    )

    class Meta:
        verbose_name_plural = "Receptive Games Images"

    def __str__(self) -> str:
        return f"Image For {self.receptive.level}'s Recetive Game"


class Expressive(models.Model):
    img = models.ImageField(upload_to="level/expressive")
    answer = models.CharField(max_length=255)
    level = models.OneToOneField(Level, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Expressive Games"

    def __str__(self) -> str:
        return f"{self.level}'s Expressive Game"


class Social(models.Model):
    video = models.FileField(upload_to="level/social")
    level = models.OneToOneField(Level, on_delete=models.CASCADE)

    # messages
    class Meta:
        verbose_name_plural = "Social Games"

    def __str__(self) -> str:
        return f"{self.level}'s Social Game"


class conversionMessage(models.Model):
    message = models.CharField(max_length=100)
    social = models.ForeignKey(
        Social, on_delete=models.CASCADE, related_name="messages"
    )

    class Meta:
        verbose_name_plural = "Social Games Messages"

    def __str__(self) -> str:
        return f"Message For {self.social.level}"
