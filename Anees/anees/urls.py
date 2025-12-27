from django.urls import path
from . import views


urlpatterns = [
    path("children/", views.ChildrenListApiView.as_view(), name="children-list"),
    path(
        "children/<int:pk>/",
        views.ChildrenProfilesApiView.as_view(),
        name="child-profiles",
    ),
    path(
        "children/<int:pk>/words/",
        views.ChildrenProfilesWordsApiView.as_view(),
        name="child-profiles",
    ),
    path("children/me/", views.ChildDetailApiView.as_view(), name="child-detail"),
    path("children/me/words/", views.ChildWordsApiView.as_view(), name="child-words"),
    path("levels/", views.LevelListApiView.as_view(), name="levels-list"),
    path("levels/<int:pk>/", views.LevelDetailApiView.as_view(), name="level-detail"),
    path(
        "levels/<int:pk>/receptive/", views.ReceptiveApiView.as_view(), name="receptive"
    ),
    path(
        "levels/<int:pk>/expressive/",
        views.ExpressiveApiView.as_view(),
        name="expressive",
    ),
    path("levels/<int:pk>/social/", views.SocialApiView.as_view(), name="social"),
    path("predict/", views.AIModelApiView.as_view(), name="predict"),
]
