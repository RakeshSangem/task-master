from rest_framework import serializers
from .models import Todo


class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = ['id', 'uid', 'title', 'description', 'completed',
                  'due_date', 'priority', 'created_at', 'updated_at']
        read_only_fields = ['id', 'uid', 'created_at', 'updated_at']
