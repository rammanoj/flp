import random
from _sha256 import sha256
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.db import transaction
from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from accounts.mails import main as sendinvite
from . import serializers
from . import models
from accounts import mails
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView, DestroyAPIView
from flp.settings import FRONTEND_URL
from rest_framework import pagination


# Team Views
class TeamCreateView(CreateAPIView):
    serializer_class = serializers.TeamSerializer
    queryset = models.Team.objects.all()

    def post(self, request, *args, **kwargs):
        request.data['created_by'] = request.user.pk
        request.data['user'] = {}
        return super(TeamCreateView, self).post(request, *args, *kwargs)


class TeamListView(ListAPIView):
    serializer_class = serializers.TeamSerializer
    pagination_class = None

    def get_queryset(self):
        return models.Team.objects.filter(user=self.request.user)

    def get(self, request, *args, **kwargs):
        context = super(TeamListView, self).get(request, *args, **kwargs)
        data = context.data
        del context.data
        context.data = {}
        context.data['results'] = data
        return context


class TeamRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.TeamSerializer
    queryset = models.Team.objects.all()
    http_method_names = ['patch', 'delete', 'get']
    
    def get(self, request, *args, **kwargs):
        if request.user not in self.get_object().user.all():
            return Response({'message': 'Permission denied', 'error': 1}, status=status.HTTP_400_BAD_REQUEST)
        return super(TeamRetrieveUpdateDestroyView, self).get(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        if request.user != self.get_object().created_by:
            return Response({'message': 'Permission denied', 'error': 1}, status=status.HTTP_400_BAD_REQUEST)
        return super(TeamRetrieveUpdateDestroyView, self).patch(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        if request.user != self.get_object().created_by:
            return Response({'message': 'Permission denied', 'error': 1}, status=status.HTTP_400_BAD_REQUEST)
        super(TeamRetrieveUpdateDestroyView, self).delete(request, *args, **kwargs)
        return Response({'message': 'Successfully deleted', 'error': 0})


class TeamAddUser(APIView):
    http_method_names = ['get', 'post']

    def get(self, request, *args, **kwargs):
        try:
            link = request.GET.get('link', None)
        except KeyError:
            return Response({'message': 'Invalid Link', 'error': 1}, status=status.HTTP_400_BAD_REQUEST)

        link = models.InviteLink.objects.filter(link=link)
        if link.exists():
            user = models.InviteLinkUsers.objects.filter(link=link[0])
            if user.filter(user=request.user).exists():
                return Response({'message': 'Valid Link', 'error': 0})
            else:
                return Response({'message': 'Invalid Link', 'error': 1}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'message': 'Invalid Link', 'error': 1}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, *args, **kwargs):
        try:
            data = request.data['email']
            team = get_object_or_404(models.Team, pk=request.data['team'])
        except KeyError:
            return Response({'message': 'Enter all the details', 'error': 1}, status=status.HTTP_400_BAD_REQUEST)
        if len(data) == 0:
            return Response({'message': 'Enter any email', 'error': 1}, status=status.HTTP_400_BAD_REQUEST)

        if request.user not in team.user.all():
            return Response({'message': 'Permission denied', 'error': 1}, status=status.HTTP_400_BAD_REQUEST)

        temp, mails, bcc, to_mail, email, users = 0, [], [], '', '', []
        for i in data:
            try:
                validate_email(i)
            except (KeyError, ValidationError) as e:
                continue

            check = User.objects.filter(email=i)
            if check.exists() and check[0] not in team.user.all():
                users.append(check[0])
                if temp == 0:
                    to_mail = i
                else:
                    bcc.append(i)

            if temp == 0:
                temp = 1

        # Create a Invite link ot the Invited people.
        hash_code = sha256((str(random.getrandbits(256)) + to_mail).encode('utf-8')).hexdigest()
        link = models.InviteLink.objects.create(team=team, link=hash_code)
        # Restrict the users to the link.

        for i in users:
            models.InviteLinkUsers.objects.create(link=link, user=i)

        args = []
        kwargs = {
            'mail_type': 3,
            'bcc': bcc,
            'invitelink': hash_code,
            'team': team.name
        }
        sent = sendinvite(to_mail=to_mail, *args, **kwargs)
        if sent == 1:
            return Response({'message': 'Invitation link sent to the users successfully.', 'error': 0})
        else:
            return Response({'message': 'Failed in sending Invitation links, try again later', 'error': 1}, status=status.HTTP_400_BAD_REQUEST)


class TeamAddorRemoveUser(APIView):

    def post(self, request, *args, **kwargs):
        try:
            operation = request.data['operation']

            if operation == "Add":
                confirm = request.data['confirm']
                link = request.data['link']
                link = get_object_or_404(models.InviteLink, link=link)
                users = models.InviteLinkUsers.objects.filter(link=link)
                if not users.exists():
                    link.delete()
                    return Response({'message': 'Link not Found', 'error': 1}, status=status.HTTP_404_NOT_FOUND)
                user = users.filter(user=request.user)
                if not user.exists():
                    return Response({'message': 'Link not found', 'error': 1}, status=status.HTTP_400_BAD_REQUEST)
                if confirm is True:
                    # Add user to the team
                    with transaction.atomic():
                        team = link.team
                        team.user.add(request.user)
                        team.save()
                        text = request.user.username + ' joined the group'
                        models.Notification.objects.create(group=team, text=text)
                        user.delete()
                        if not users.exists():
                            link.delete()
                    return Response({'message': 'Added you to the group', 'error': 0})
                else:
                    user.delete()
                    if not users.exists():
                        link.delete()
                    return Response({'message': '', 'error': 0})
            elif operation == "Remove":
                team = get_object_or_404(models.Team, pk=request.data['team'])
                if team.created_by == request.user:
                    return Response({"message": "Creator of group, can not exit group", "error": 1}, status=status.HTTP_400_BAD_REQUEST)

                with transaction.atomic():
                    team.user.remove(request.user)
                    text = request.user.username + ' exited the group'
                    models.Notification.objects.create(group=team, text=text)

                return Response({'message': 'Successfully exited from the group', 'error': 0})
            else:
                return Response({'message': 'Invalid operation', 'error': 1}, status=status.HTTP_400_BAD_REQUEST)

        except KeyError:
            return Response({'message': 'Fill all the details', 'error': 1}, status=status.HTTP_400_BAD_REQUEST)


class UserTeamListView(ListAPIView):
    serializer_class = serializers.TeamSerializer

    def get_queryset(self):
        return models.Team.objects.filter(user=self.request.user)


class TeamUserListView(ListAPIView):
    serializer_class = serializers.UserSerializer
    queryset = models.User.objects.all()

    def get(self, request, *args, **kwargs):
        try:
            team = get_object_or_404(models.Team, pk=self.kwargs['pk'])
        except KeyError:
            return Response({'error': 1, 'message': 'Error in fetching details'}, status=status.HTTP_400_BAD_REQUEST)

        if request.user not in team.user.all():
            return Response({'message': 'Permission Denied', 'error': 1}, status=status.HTTP_400_BAD_REQUEST)

        self.queryset = team.user.all()
        return super(TeamUserListView, self).get(request, *args, **kwargs)


class TeamUserDeleteView(DestroyAPIView):

    def delete(self, request, *args, **kwargs):
        user = get_object_or_404(User, pk=self.kwargs['user'])
        team = get_object_or_404(models.Team, pk=self.kwargs['pk'])

        if team.created_by != request.user:
            return Response({'message': 'Permission denied', 'error': 1}, status=status.HTTP_400_BAD_REQUEST)

        if team.created_by == user:
            return Response({'message': 'You can not delete yourself from team', 'error': 1}, status=status.HTTP_400_BAD_REQUEST)
        team.user.remove(user)
        return Response({'message': 'Successfully removed', 'error': 0})

# End of Team Views


class PostCreateView(CreateAPIView):
    serializer_class = serializers.PostSerializer
    queryset = models.Post.objects.all()
    
    def post(self, request, *args, **kwargs):
        try:
            team = get_object_or_404(models.Team, pk=request.data['team'])
            if request.user not in team.user.all():
                return Response({'message': 'Permission denied', 'error': 1}, status=status.HTTP_400_BAD_REQUEST)

        except KeyError:
            return Response({'message': "Fill the form completely", 'error': 1}, status=status.HTTP_400_BAD_REQUEST)

        request.data._mutable = True
        request.data['created_by'] = request.user.pk
        request._mutable = False
        context = super(PostCreateView, self).post(request, *args, **kwargs)

        # Add Notification
        text = request.user.username + ' posted ' + context.data['header']
        link = FRONTEND_URL + "group/" + str(team.pk) + "/post/" + str(context.data['pk'])
        models.Notification.objects.create(group=team, text=text, link=link)

        # Send Mail
        members = team.user.all().exclude(pk=request.user.pk)
        members = list(members.values_list('email', flat=True))
        if len(members) > 0:
            to_mail = members.pop(0)
            kwargs = {'mail_type': 4, 'bcc': members, 'group': team.name, 'user': request.user.username, 'link': link}
            args = []
            mails.main(to_mail=to_mail, *args, **kwargs)
        return context


class PostRetrieveUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.PostSerializer
    queryset = models.Post.objects.all()
    http_method_names = ['patch', 'delete']

    def patch(self, request, *args, **kwargs):
        if request.user != self.get_object().created_by:
            return Response({'message': 'Permission denied', 'error': 1}, status=status.HTTP_400_BAD_REQUEST)
        context = super(PostRetrieveUpdateDeleteView, self).patch(request, *args, **kwargs)

        # Notification
        text = request.user.username + ' posted ' + context.data['header']
        link = FRONTEND_URL + "group/" + str(context.data['team']) + "/post/" + str(context.data['pk'])
        models.Notification.objects.create(group=self.get_object().team, text=text, link=link)

        # Mail notify
        members = self.get_object().team.user.all().exclude(pk=request.user.pk)
        members = list(members.values_list('email', flat=True))
        print(members)
        if len(members) > 0:
            to_mail = members.pop(0)
            args = []
            kwargs = {'mail_type': 5, 'bcc': members, 'group': self.get_object().team.name,
                                    'user': request.user.username, 'link': link, 'post': self.get_object().header}
            mails.main(to_mail=to_mail, *args, **kwargs)
        return context

    def delete(self, request, *args, **kwargs):
        if request.user != self.get_object().created_by:
            return Response({'message': 'Permission denied', 'error': 1}, status=status.HTTP_400_BAD_REQUEST)
        super(PostRetrieveUpdateDeleteView, self).delete(request, *args, **kwargs)
        return Response({'message': 'Successfully deleted', 'error': 0})


class PostListView(ListAPIView):
    serializer_class = serializers.PostSerializer
    pagination_class = pagination.PageNumberPagination
    pagination_class.page_size = 25

    def get_queryset(self):
        search = self.request.GET.get('search', None)
        name = self.request.GET.get('name', None)
        if search is None or name is None:
            return models.Post.objects.filter(team__pk=self.kwargs['pk']).order_by('-created_on')
        else:
            kwargs = {
                'team__pk': self.kwargs['pk']
            }
            if name is 'pk':
                kwargs['name'] = search
            else:
                kwargs[name + '__contains'] = search
            return models.Post.objects.filter(**kwargs).order_by('-created_on')

    def get(self, request, *args, **kwargs):
        if request.user not in get_object_or_404(models.Team, pk=self.kwargs['pk']).user.all():
            return Response({'message': 'Permission denied', 'error': 1}, status=status.HTTP_400_BAD_REQUEST)

        context = super(PostListView, self).get(request, *args, **kwargs)
        return context


class UpdatePostAction(APIView):
    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        post = get_object_or_404(models.Post, pk=self.kwargs['pk'])
        if request.user not in post.team.user.all():
            return Response({'message': 'permission denied', 'error': 1}, status=status.HTTP_400_BAD_REQUEST)

        try:
            action = request.data['action']
            pa = models.PostAction.objects.filter(Q(user=request.user), Q(post=post)).order_by('-created_on')
            if pa.exists():
                pa = pa[0]
                if action == '':
                    pa.delete()
                else:
                    pa.action = action
                    pa.save()
            else:
                models.PostAction.objects.create(user=request.user, action=action, post=post)
                act = "dislike"
                if action == "like":
                    act = "like"
                text = request.user.username + ' ' + act + ' ' + ' post ' + pa[0].post.header
                link = FRONTEND_URL + "group/" + str(pa[0].post.team.pk) + "/post/" + str(pa[0].post.pk)
                models.Notification.objects.create(group=pa[0].post.team, text=text, link=link)
        except KeyError:
            return Response({'message': 'Fill all details', 'error' :1}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'error': 0})


class CommentCreateView(CreateAPIView):
    serializer_class = serializers.CommentSerializer
    queryset = models.Post.objects.all()

    def post(self, request, *args, **kwargs):
        post = get_object_or_404(models.Post, pk=self.kwargs['pk'])
        if request.user not in post.team.user.all():
            return Response({'message': 'Permission denied', 'error': 1}, status=status.HTTP_400_BAD_REQUEST)
        request.data['user'] = request.user.pk
        request.data['post'] = post.pk
        context = super(CommentCreateView, self).post(request, *args, **kwargs)
        text = request.user.username + ' commented on post ' + post.header
        link = FRONTEND_URL + "group/" + str(post.team.pk) + "/post/" + str(post.pk)
        models.Notification.objects.create(group=post.team, text=text, link=link)
        return context


class CommentListView(ListAPIView):
    serializer_class = serializers.CommentSerializer

    def get_queryset(self):
        return models.PostComment.objects.filter(post__pk=self.kwargs['pk'])

    def get(self, request, *args, **kwargs):
        post = get_object_or_404(models.Post, pk=self.kwargs['pk'])
        if request.user not in post.team.user.all():
            return Response({'message': 'Permission denied', 'error': 1}, status=status.HTTP_400_BAD_REQUEST)
        return super(CommentListView, self).get(request, *args, **kwargs)


class CommentRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.CommentSerializer
    queryset = models.PostComment.objects.all()
    http_method_names = ['patch', 'delete']

    def patch(self, request, *args, **kwargs):
        if request.user != self.get_object().user:
            return Response({'message': 'Permission denied', 'error': 1}, status=status.HTTP_400_BAD_REQUEST)
        return super(CommentRetrieveUpdateDestroyView, self).patch(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        if request.user != self.get_object().user:
            return Response({'message': 'Permission denied', 'error': 1}, status=status.HTTP_400_BAD_REQUEST)
        super(CommentRetrieveUpdateDestroyView, self).delete(request, *args, **kwargs)
        return Response({'message': 'Successfully deleted', 'error': 0})


class ReCommentCreateView(CreateAPIView):
    serializer_class = serializers.ReCommentSerializer

    def get_queryset(self):
        return models.PostReComment.objects.all()

    def post(self, request, *args, **kwargs):
        comment = get_object_or_404(models.PostComment, pk=self.kwargs['pk'])
        if request.user not in comment.post.team.user.all():
            return Response({'message': 'Permission denied', 'error': 1}, status=status.HTTP_400_BAD_REQUEST)
        request.data['user'] = request.user.pk
        request.data['comment'] = self.kwargs['pk']
        return super(ReCommentCreateView, self).post(request, *args, **kwargs)


class ReCommentRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.ReCommentSerializer
    queryset = models.PostReComment.objects.all()
    http_method_names = ['patch', 'delete']

    def patch(self, request, *args, **kwargs):
        if request.user != self.get_object().user:
            return Response({'message': 'Permission denied', 'error': 1}, status=status.HTTP_400_BAD_REQUEST)
        return super(ReCommentRetrieveUpdateDestroyView, self).patch(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        if request.user != self.get_object().user:
            return Response({'message': 'Permission denied', 'error': 1}, status=status.HTTP_400_BAD_REQUEST)
        super(ReCommentRetrieveUpdateDestroyView, self).delete(request, *args, **kwargs)
        return Response({'message': 'Successfully deleted', 'error': 0})


class RecentNotifications(ListAPIView):
    serializer_class = serializers.NotificationSerializer

    def get_queryset(self):
        return models.Notification.objects.filter(group__pk=self.kwargs['pk'])


class Actionusers(ListAPIView):
    serializer_class = serializers.PostActionSerializer

    def get_queryset(self):
        return models.PostAction.objects.filter(Q(team=self.kwargs['team']), Q(action=self.kwargs['action']))
