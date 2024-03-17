from rest_framework import serializers
import requests

from rest_framework import serializers
import requests

from repository.models import Entrys, Project

class RetrieveCodeFromGithubSerializer(serializers.Serializer):
    github_username = serializers.CharField(max_length=100)
    github_repository = serializers.CharField(max_length=100)

    def validate(self, data):
        # Validación de campos
        github_username = data['github_username']
        if not github_username:
            raise serializers.ValidationError("El nombre de usuario de Github es obligatorio.")

        github_repository = data['github_repository']
        if not github_repository:
            raise serializers.ValidationError("El nombre del repositorio de Github es obligatorio.")

        return data

    def save(self):
        github_username = self.validated_data['github_username']
        github_repository = self.validated_data['github_repository']

        # Obtener datos de la sesión
        user_data = self.context['request'].session.get('user')
        print('dataraaaaa',user_data)
        # Extraer información relevante
        github_access_token = user_data.get('access_token')  # Adaptar según la estructura de la sesión

        # Construir headers
        headers = {}
        if github_access_token:
            headers['Authorization'] = f"token {github_access_token}"

        # Preparar URL
        url = f"https://api.github.com/repos/{github_username}/{github_repository}/contents"

        # Realizar la solicitud
        response = requests.get(url, headers=headers)


        if response.status_code == 200:
            return response.json()
        elif response.status_code == 401:
            raise serializers.ValidationError("Acceso denegado. Revise las credenciales de Github.")
        else:
            raise serializers.ValidationError(f"Error al obtener el código: {response.status_code}")


class EntrysSerializer(serializers.ModelSerializer):
    class Meta:
        model = Entrys  # Corregir el modelo a Entrys
        fields = '__all__'
        read_only_fields = ('user', 'created_at')
        extra_kwargs = {
            'name': {'required': True}
        }

        
class ProjectSerializer(serializers.ModelSerializer):
    entries = EntrysSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = '__all__'
        read_only_fields = ('user', 'created_at')
        extra_kwargs = {
            'name': {'required': True}
        }
    
    def create(self, validated_data):
        return super().create(validated_data)


