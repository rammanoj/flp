import random
from _sha256 import sha256

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from accounts.mails import main as sendinvite
from . import serializers
from . import models
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView, DestroyAPIView


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

    def get_queryset(self):
        return models.Team.objects.filter(user=self.request.user)


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

        if team.created_by != request.user:
            return Response({'message': 'Permission denied', 'error': 1}, status=status.HTTP_400_BAD_REQUEST)

        temp, mails, bcc, to_mail, email, users = 0, [], [], '', '', []
        for i in data:
            try:
                validate_email(i)
            except (KeyError, ValidationError) as e:
                continue

            check = User.objects.filter(email=i)
            if check.exists():
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
                        user.delete()
                    return Response({'message': 'Added you to the group', 'error': 0})
                else:
                    user.delete()
                    return Response({'message': '', 'error': 0})
            elif operation == "Remove":
                team = get_object_or_404(models.Team, pk=request.data['team'])
                if team.created_by == request.user:
                    return Response({"message": "Creator of group, can not exit group", "error": 1}, status=status.HTTP_400_BAD_REQUEST)
                team.user.remove(request.user)
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
            return Response({'message': 'Permission denied', 'error': 1}, status=status.HTTP_400_BAD_REQUEST)

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


