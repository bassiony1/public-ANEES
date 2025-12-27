from djoser.views import UserViewSet as BaseUserViewSet
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle


class AnonUserCreateAccountThrottle(AnonRateThrottle):
    THROTTLE_RATES = {"anon": "10/day"}


class NonAnonUserCreateAccountThrottle(UserRateThrottle):
    THROTTLE_RATES = {"user": "5/day"}


class UserViewSet(BaseUserViewSet):
    def get_throttles(self):
        if self.action == "create":
            return super().get_throttles()  # Remove this line in production
            return [AnonUserCreateAccountThrottle(), NonAnonUserCreateAccountThrottle()]
        return super().get_throttles()
