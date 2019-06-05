from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
from flp.settings import FRONTEND_URL, BASE_URL
from django.db.models import Q
from . import models
from rest_framework import serializers
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    pic = serializers.SerializerMethodField()

    def get_pic(self, obj):
        try:
            rv = BASE_URL[:-1] + obj.profile.pic.url
            return rv
        except (ObjectDoesNotExist, ValueError):
            return ""

    class Meta:
        model = User
        fields = ['username', 'pk', 'pic']
        read_only_fields = ['username', 'pk', 'pic']


class SubGroup(serializers.ModelSerializer):

    def to_representation(self, instance):
        data = super(SubGroup, self).to_representation(instance)
        user = User.objects.filter(pk=data['created_by'])
        if user.exists():
            data['created_by'] = user[0].username
        return data

    def create(self, validated_data):
        return super(SubGroup, self).create(validated_data)

    class Meta:
        model = models.SubGroup
        fields = ['pk', 'name', 'team', 'created_on', 'created_by']
        read_only_fields = ['pk', 'created_on']


class TeamSerializer(serializers.ModelSerializer):
    edit = serializers.SerializerMethodField()
    subgroup_set = SubGroup(many=True, read_only=True)
    pic = serializers.FileField(required=False)

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

        # Add a main Subgroup
        models.SubGroup.objects.create(name='main', team=context, created_by=self.context['request'].user)
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
        fields = ['name', 'about', 'created_by', 'subgroup_set', 'created_on', 'edit', 'pk', 'pic']
        read_only_fields = ['pk', 'created_on', 'user', 'subgroup_set']


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
    created_by_pic = serializers.SerializerMethodField()

    def get_created_by_pic(self, obj):
        try:
            rv = BASE_URL[:-1] + obj.user.profile.pic.url
            return rv
        except (ObjectDoesNotExist, ValueError):
            return ''

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
        fields = ['pk', 're_comment', 'user', 'created_on', 'comment', 'edit', 'created_by_pic']
        read_only_fields = ['pk', 'created_on']


class CommentSerializer(serializers.ModelSerializer):
    edit = serializers.SerializerMethodField()
    postrecomment_set = ReCommentSerializer(many=True, read_only=True)
    created_by_pic = serializers.SerializerMethodField()

    def get_created_by_pic(self, obj):
        try:
            rv = BASE_URL[:-1] + obj.user.profile.pic.url
            return rv
        except (ObjectDoesNotExist, ValueError):
            return ''

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
        fields = ['comment', 'post', 'postfile', 'created_on', 'user', 'pk', 'edit', 'postrecomment_set', 'created_by_pic']
        read_only_fields = ['created_on', 'pk', 'edit', 'postrecomment_set']


class TaggedUser(serializers.ModelSerializer):

    def to_representation(self, instance):
        context = super(TaggedUser, self).to_representation(instance)
        context['user'] = get_object_or_404(User, pk=context['user']).username
        return context

    class Meta:
        model = models.PostTaggedUser
        fields = ['user']


class PostFile(serializers.ModelSerializer):

    def to_representation(self, instance):
        context = super(PostFile, self).to_representation(instance)
        context['file'] = BASE_URL[:-1] + instance.file.url
        context['name'] = instance.file.name
        return context

    class Meta:
        model = models.PostFile
        fields = ['pk', 'file']


class PostSerializer(serializers.ModelSerializer):
    edit = serializers.SerializerMethodField()
    like = serializers.SerializerMethodField()
    action = serializers.SerializerMethodField()
    link = serializers.SerializerMethodField()
    posttaggeduser_set = TaggedUser(many=True, read_only=True)
    created_by_pic = serializers.SerializerMethodField()
    postfile_set = PostFile(many=True, read_only=True)

    def get_created_by_pic(self, obj):
        try:
            rv = BASE_URL[:-1] + obj.created_by.profile.pic.url
            return rv
        except (ObjectDoesNotExist, ValueError):
            return ''

    def get_link(self, obj):
        return FRONTEND_URL + "group/" + str(obj.group.team.pk) + "/" + str(obj.group.pk) + "/post/" + str(obj.pk) + "/"

    def get_action(self, obj):
        elem = obj.postaction_set.all().filter(user=self.context['request'].user)
        if elem.exists():
            return elem[0].action
        else:
            return ""

    def to_representation(self, instance):
        data = super(PostSerializer, self).to_representation(instance)
        user = User.objects.filter(pk=data['created_by'])
        if user.exists():
            data['created_by'] = user[0].username
        return data

    def get_like(self, obj):
        return len(models.PostAction.objects.filter(Q(post=obj), Q(action="like")))

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
            context = super(PostSerializer, self).update(instance, validated_data)
            return context


    class Meta:
        model = models.Post
        fields = ['header', 'created_by', 'created_on', 'about', 'group',
                  'pk', 'action', 'edit', 'like', 'link', 'posttaggeduser_set', 'created_by_pic', 'postfile_set']
        read_only_fields = ['created_on', 'pk', 'comments', 'like', 'action', 'link', 'posttaggeduser_set', 'postfile_set']


class NotificationSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Notification
        fields = '__all__'

