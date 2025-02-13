from rest_framework import serializers
from .models import ThemeConfiguration

class ThemeConfigurationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ThemeConfiguration
        fields = [
            'role',
            'primary_color',
            'secondary_color',
            'background_color',
            'text_color',
        ]