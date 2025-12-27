from django.db.models.signals import post_save
from django.contrib.auth import get_user_model
from django.dispatch import receiver
from .models import Child, ChildLevel, Level
from django.db.models import Q

User = get_user_model()


@receiver(post_save, sender=User)
def create_Child_profile(sender, instance, created, **kwargs):
    if created:
        Child.objects.create(user=instance)


@receiver(post_save, sender=Child)
def Create_ChildLevel(sender, instance, created, **kwargs):
    if created:
        if Level.objects.filter(level_num=1).exists():
            ChildLevel.objects.create(
                child=instance, level=Level.objects.get(level_num=1)
            )


@receiver(post_save, sender=Level)
def assign_user_new_level(sender, instance, created, **kwargs):
    if created:
        children = []
        if instance.level_num == 1:
            children = Child.objects.all()

            if children:
                for child in children:
                    ChildLevel.objects.create(child=child, level=instance)
                # ChildLevel.objects.bulk_create(
                #     [ChildLevel(child=child, level=instance) for child in children]
                # )
        else:
            children = (
                ChildLevel.objects.select_related("child")
                .filter(
                    level__level_num=instance.level_num - 1,
                    receptive_complete=True,
                    expressive_complete=True,
                    social_complete=True,
                )
                .values_list("child", flat=True)
            )
            if children:
                for child_id in children:
                    ChildLevel.objects.create(child_id=child_id, level=instance)
                # ChildLevel.objects.bulk_create(
                #     [
                #         ChildLevel(child_id=child_id, level=instance)
                #         for child_id in children
                #     ]
                # )


@receiver(post_save, sender=ChildLevel)
def update_level(sender, instance, created, **kwargs):
    if created:
        level = instance.level
        try:
            if level.receptive:
                pass
        except:
            instance.receptive_complete = True
            instance.receptive_score = 100

        try:
            if level.expressive:
                pass
        except:
            instance.expressive_complete = True
            instance.expressive_score = 100

        try:
            if level.social:
                pass
        except:
            instance.social_complete = True
            instance.social_score = 100

        instance.save()
