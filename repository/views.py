import requests
from rest_framework import (viewsets, status)
from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.response import Response
# from core.models import (Project )
from drf_spectacular.utils import extend_schema_view, extend_schema
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema_view, extend_schema, OpenApiParameter ,extend_schema_field



from repository import serializers
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
)

from repository.models import Project


@extend_schema_field(OpenApiTypes.BYTE) 
class RetrieveInfoFromGithub(viewsets.GenericViewSet):
    serializer_class = serializers.RetrieveCodeFromGithubSerializer

    @extend_schema(description='text')
    @action(detail=False, methods=['get'])
    def get_info(self, request):
        github_username = request.query_params.get('github_username')
        github_repository = request.query_params.get('github_repository')
        
        github_username = 'tonderflash'
        github_repository = 'tonderflash'
        github_repository_path = 'README.md'
        
        if not github_username or not github_repository:
            return Response("Missing 'github_username' or 'github_repository' query parameters", 
                            status=status.HTTP_400_BAD_REQUEST)

        # Access session data
        user_data = request.session.get('user')

        if not user_data:
            return Response("User session data not found", status=status.HTTP_400_BAD_REQUEST)

        github_access_token = user_data.get('access_token')

        # GitHub API Request
        headers = {}
        if github_access_token:
            headers['Accept'] = 'application/vnd.github+json'
            headers['Authorization'] = f"Bearer {github_access_token}"

        url = f"https://api.github.com/repos/{github_username}/{github_repository}/contents/{github_repository_path}"
        
        response = requests.get(url, headers=headers)
        print('response',response)
        if response.status_code == 200:
            return Response(response.json(), status=status.HTTP_200_OK)
        else:
            return Response(f"Failed to retrieve code: {response.status_code}", 
                            status=response.status_code)


    @action(detail=False, methods=['get'])
    def get_user(self, request):
        user_data = request.session.get('user')
        return Response(user_data, status=status.HTTP_200_OK)


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = serializers.ProjectSerializer

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)
    

    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    