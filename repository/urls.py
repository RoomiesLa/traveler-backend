
from django.urls import (
    path,
    include
)

from rest_framework.routers import DefaultRouter

from repository import views

router = DefaultRouter()
app_name = 'repository'

router.register('projects', views.ProjectViewSet)
router.register('github', views.RetrieveInfoFromGithub, basename='github')

urlpatterns = [
    path('', include(router.urls))
]
