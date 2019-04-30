from . import models
from rest_framework import serializers
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['username', 'email', 'pk']
        read_only_fields = ['username', 'email', 'pk']


class TeamSerializer(serializers.ModelSerializer):
    edit = serializers.SerializerMethodField()
    user = UserSerializer(read_only=True)

    def get_edit(self, obj):
        return obj.created_by == self.context['request'].user

    def validate_name(self, name):
        if len(name) < 6:
            raise serializers.ValidationError('min length is 8')
        return name

    def create(self, validated_data):
        context = super(TeamSerializer, self).create(validated_data)
        context.user.add(self.context['request'].user)
        return context

    def update(self, instance, validated_data):
        if self.context['request'].user != instance.created_by:
            raise serializers.ValidationError('permission denied')
        else:
            try:
                del validated_data['created_by']
            except KeyError:
                pass
            return super(TeamSerializer, self).update(instance, validated_data)

    class Meta:
        model = models.Team
        fields = ['name', 'about', 'created_by', 'created_on', 'user', 'edit', 'pk']
        read_only_fields = ['pk', 'created_on', 'user']