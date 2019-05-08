import datetime

from django.db import transaction
from django.db.models import Q

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

    def to_representation(self, instance):
        data = super(TeamSerializer, self).to_representation(instance)
        user = User.objects.filter(pk=data['created_by'])
        if user.exists():
            data['created_by'] = user[0].username
        return data

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
        fields = ['name', 'about', 'created_by', 'created_on', 'edit', 'pk']
        read_only_fields = ['pk', 'created_on', 'user']


class PostActionSerializer(serializers.ModelSerializer):

    def to_representation(self, instance):
        data = super(PostActionSerializer, self).to_representation(instance)
        data['user'] = User.objects.get(pk=data['user']).username
        return data

    class Meta:
        model = models.PostAction
        fields = ['action', 'user']


class ReCommentSerializer(serializers.ModelSerializer):
    edit = serializers.SerializerMethodField()

    def get_edit(self, obj):
        return obj.user == self.context['request'].user

    def to_representation(self, instance):
        data = super(ReCommentSerializer, self).to_representation(instance)
        user = User.objects.filter(pk=data['user'])
        if user.exists():
            data['user'] = user[0].username
        return data

    def create(self, validated_data):
        return super(ReCommentSerializer, self).create(validated_data)

    def update(self, instance, validated_data):
        if self.context['request'].user != instance.user:
            raise serializers.ValidationError('permission denied')
        else:
            try:
                del validated_data['created_by']
            except KeyError:
                pass
            return super(ReCommentSerializer, self).update(instance, validated_data)

    class Meta:
        model = models.PostReComment
        fields = ['pk', 're_comment', 'user', 'created_on', 'comment', 'edit']
        read_only_fields = ['pk', 'created_on']


class CommentSerializer(serializers.ModelSerializer):
    edit = serializers.SerializerMethodField()
    postrecomment_set = ReCommentSerializer(many=True, read_only=True)

    def get_edit(self, obj):
        return obj.user == self.context['request'].user

    def create(self, validated_data):
        return super(CommentSerializer, self).create(validated_data)

    def to_representation(self, instance):
        data = super(CommentSerializer, self).to_representation(instance)
        user = User.objects.filter(pk=data['user'])
        if user.exists():
            data['user'] = user[0].username
        return data

    def update(self, instance, validated_data):
        if self.context['request'].user != instance.user:
            raise serializers.ValidationError('permission denied')
        else:
            try:
                del validated_data['created_by']
            except KeyError:
                pass
            return super(CommentSerializer, self).update(instance, validated_data)

    class Meta:
        model = models.PostComment
        fields = ['comment', 'post', 'created_on', 'user', 'pk', 'edit', 'postrecomment_set']
        read_only_fields = ['created_on', 'pk', 'edit', 'postrecomment_set']


class PostSerializer(serializers.ModelSerializer):
    edit = serializers.SerializerMethodField()
    like = serializers.SerializerMethodField()
    unlike = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()
    action = serializers.SerializerMethodField()

    def get_action(self, obj):
        print(self.context['request'].user)
        print(obj.postaction_set.all())
        elem = obj.postaction_set.all().filter(user=self.context['request'].user)
        print(elem)
        if elem.exists():
            return elem[0].action
        else:
            return ""

    def get_comments(self, obj):
        queryset = obj.postcomment_set.all()[:3]
        return CommentSerializer(queryset, many=True, context=self.context).data

    def to_representation(self, instance):
        data = super(PostSerializer, self).to_representation(instance)
        user = User.objects.filter(pk=data['created_by'])
        if user.exists():
            data['username'] = user[0].username
        return data

    def get_like(self, obj):
        return len(models.PostAction.objects.filter(Q(post=obj), Q(action="like")))

    def get_unlike(self, obj):
        return len(models.PostAction.objects.filter(Q(post=obj), Q(action="unlike")))

    def get_edit(self, obj):
        return obj.created_by == self.context['request'].user

    def get_ca(self, obj):
        pa = models.PostAction.objects.filter(post=obj)
        if pa.exists():
            return pa
        else:
            return ""

    def validate_header(self, header):
        if len(header) < 6:
            raise serializers.ValidationError('min length is 6')
        return header

    def create(self, validated_data):
        return super(PostSerializer, self).create(validated_data)

    def update(self, instance, validated_data):
        if self.context['request'].user != instance.created_by:
            raise serializers.ValidationError('permission denied')
        else:
            try:
                del validated_data['created_by']
            except KeyError:
                pass
            return super(PostSerializer, self).update(instance, validated_data)

    class Meta:
        model = models.Post
        fields = ['file', 'header', 'created_by', 'created_on', 'about', 'team',
                  'pk', 'action', 'edit', 'comments', 'like', 'unlike']
        read_only_fields = ['created_on', 'pk', 'comments', 'like', 'unlike', 'action']


class NotificationSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Notification
        fields = '__all__'
        read_only_fields = '__all__'

