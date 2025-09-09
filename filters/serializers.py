from rest_framework import serializers
from .models import UserFilter


class UserFilterSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserFilter
        fields = "__all__"
        read_only_fields = ["user"]

    def create(self, validated_data):
        user = self.context['request'].user
        # Update if filter exists, else create
        obj, created = UserFilter.objects.update_or_create(user=user, defaults=validated_data)
        return obj
