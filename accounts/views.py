import datetime, random
from _sha256 import sha256
from json import loads
from django.contrib.auth import authenticate, login
from django.core.validators import validate_email
from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import get_object_or_404, render
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from knox.views import LoginView, LogoutView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView, UpdateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ValidationError
from rest_framework.views import APIView
from accounts import models, serializers, mails
from knox.models import AuthToken


# User Registration
class UserCreateView(CreateAPIView):
    permission_classes = []
    authentication_classes = []
    serializer_class = serializers.UserSerializer

    def get_queryset(self):
        return User.objects.all()

    def create(self, request, *args, **kwargs):
        super(UserCreateView, self).create(request, *args, **kwargs)
        return Response({'message': 'A verification mail sent to your mail.', 'error': 0})


# User LoginView
class UserLoginView(LoginView):
    http_method_names = ['post']
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request, format=None):
        s = serializers.LoginSerializer(data=self.request.data)
        s.is_valid(raise_exception=True)
        username_or_email = s.validated_data.get('user', None)
        password = s.validated_data.get('password', None)
        remember_me = s.validated_data.get('remember_me', 0)
        user = None

        # Validate if user provided username or password.
        try:
            validate_email(username_or_email)
            username = User.objects.filter(email=username_or_email)
            getUser = username
            if username.exists():
                username_or_email = username[0].username
        except ValidationError:
            getUser = User.objects.filter(username=username_or_email)

        if getUser.exists() and getUser[0].check_password(password):
            user = getUser[0]
            mail_verify = models.MailVerification.objects.filter(Q(user=user), Q(mail_type=0))
            if mail_verify.exists():
                # User have not verified his mail, send a verification mail
                mail = mail_verify[0]
                mail.time_limit = timezone.now() + datetime.timedelta(days=1)
                mail.hash_code = sha256((str(random.getrandbits(256)) + user.email).encode('utf-8')).hexdigest()
                mail.save()
                args, kwargs = [], {'mail_type': 0, 'id': mail.hash_code}
                mails.main(to_mail=user.email, *args, **kwargs)
                return Response({'message': 'Your mail Not verified, A verification mail sent to your mail, confirm it',
                                 'error': 1}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(username=username_or_email, password=password)
        if user is None:
            return Response({'message': 'No user found as per given credentials', 'error': 1},
                            status=status.HTTP_400_BAD_REQUEST)
        login(request, user)
        context = {}
        # if remember_me == 0:
        #     context['token'] = AuthToken.objects.create(user=user, expires=datetime.timedelta(days=7))
        # else:
        #     context['token'] = AuthToken.objects.create(user=user, expires=datetime.timedelta(days=90))

        if remember_me == 0:
            context['token'] = AuthToken.objects.create(user=user, expiry=datetime.timedelta(days=7))[1]
        else:
            context['token'] = AuthToken.objects.create(user=user, expiry=datetime.timedelta(days=90))[1]
        context['error'] = 0
        context['user_id'] = user.pk
        return Response(context, status=status.HTTP_200_OK)


# Logout User
class UserLogoutView(LogoutView):
    http_method_names = ['post']

    def post(self, request, format=None):
        super(UserLogoutView, self).post(request, format=None)
        return Response({'message': 'successfully logged out!', 'error': 0})


@csrf_exempt
@api_view(['GET'])
@permission_classes([AllowAny])
def MailVerificationView(request, id):
    mail_verify = models.MailVerification.objects.filter(hash_code=id)
    if not mail_verify.exists():
        context = {'message': 'Invalid link', 'error': 1}
        return render(request, 'accounts/mail_handle.html', context)

    if mail_verify[0].time_limit < timezone.now().date():
        context = {'message': 'Your time limit exceeded, please perform the operation again', 'error': 1,
                   'title': 'Mail Verification'}
        return render(request, 'accounts/mail_handle.html', context)

    context = {'message': 'Your mail successfully verified', 'error': 0}
    if not mail_verify[0].user.is_active:
        user = mail_verify[0].user
        user.is_active = True
        user.save()
    mail_verify.delete()
    return render(request, 'accounts/mail_handle.html', context)


class UserUpdateView(RetrieveUpdateAPIView):
    serializer_class = serializers.UserSettingSerializer

    def get_queryset(self):
        return User.objects.filter(pk=self.kwargs['pk'])

    def get(self, request, *args, **kwargs):
        if self.get_object() != request.user:
            return Response({'message': 'Permission denied', 'error': 1}, status=status.HTTP_400_BAD_REQUEST)

        context = super(UserUpdateView, self).get(request, *args, **kwargs)
        return context

    def patch(self, request, *args, **kwargs):
        if self.get_object() != request.user:
            return Response({'message': 'Permission denied', 'error': 1}, status=status.HTTP_400_BAD_REQUEST)
        email_change = 0
        try:
            email = request.data['email']
            try:
                validate_email(email)
                email_change = 1
            except ValidationError:
                return Response({'message': 'enter a valid data', 'error': 1}, status=status.HTTP_400_BAD_REQUEST)
        except KeyError:
            pass

        context = super(UserUpdateView, self).patch(request, *args, **kwargs)
        context.data['message'] = 'Profile successfully updated!'
        if email_change == 1:
            context.data['message'] = 'A verification mail sent to your account, confirm it'
        return context


class UserPasswordUpdateView(UpdateAPIView):
    serializer_class = serializers.UserPasswordUpdateSerializer

    def get_object(self):
        return self.request.user

    def patch(self, request, *args, **kwargs):
        s = self.get_serializer(data=request.data)
        s.is_valid(raise_exception=True)
        if not request.user.check_password(s.validated_data['password']):
            return Response({'message': 'Enter correct current password', 'error': 1},
                            status=status.HTTP_400_BAD_REQUEST)
        user = self.get_object()
        user.set_password(s.validated_data['new_password'])
        user.save()

        # delete all the login instances of the user (except current one).

        auth_token = request.auth
        tokens = AuthToken.objects.filter(user=request.user).exclude(pk=auth_token.pk)
        tokens.delete()

        return Response({'message': 'Password successfully updated', 'error': 0})


# User Password Forgot operations.
class ForgotUserPasswordUpdateView(UpdateAPIView):
    authentication_classes = []
    permission_classes = []
    serializer_class = serializers.ForgotPasswordUpdateSerailizer
    http_method_names = ['get', 'post']

    def get_queryset(self):
        return models.MailVerification.objects.filter(hash_code=self.kwargs['id'])

    def get_object(self):
        return get_object_or_404(self.get_queryset()).user

    def get(self, request, *args, **kwargs):
        if not self.get_queryset().exists():
            context = {'message': 'No Link Found as per given requirement', 'error': 1, 'title': 'Password Updation'}
            return render(request, 'accounts/mail_handle.html', context=context)
        if self.get_queryset()[0].time_limit < timezone.now().date():
            return render(request, 'accounts/mail_handle.html', {
                'message': 'Link expired, please perform the operation again',
                'error': 1,
                'title': 'Password Updation'})

        return render(request, 'accounts/password_update.html', {'mail_code': self.kwargs['id']})

    def post(self, request, *args, **kwargs):
        self.get_object()
        if request.data['password1'] == '' or request.data['password2'] == '':
            context = {'message': 'Fill the form completely', 'error': 1, 'title': 'Password updation', 'mail_code':
                       self.kwargs['id']}
            return render(request, 'accounts/password_update.html', context)
        if len(request.data['password1']) < 8:
            context = {'message': 'Min password length is 8', 'error': 1, 'title': 'Password Updation', 'mail_code':
                self.kwargs['id']}
            return render(request, 'accounts/password_update.html', context)
        if request.data['password1'] != request.data['password2']:
            context = {'message': 'Fill the same passwords both the times', 'error': 1, 'title': 'Password updation',
                       'mail_code': self.kwargs['id']}
            return render(request, 'accounts/password_update.html', context)
        # update user
        user = self.get_object()
        user.set_password(request.data['password1'])
        user.save()
        # delete all the user logged-in instances
        AuthToken.objects.filter(user=self.get_object()).delete()
        # delete mail verification
        self.get_queryset().delete()
        context = {'message': 'Password successfully updated', 'error': 0, 'title': 'Password Updation'}
        return render(request, 'accounts/mail_handle.html', context)


# User Password Forgot operations.
@api_view(['POST'])
@csrf_exempt
@permission_classes([AllowAny])
def password_forgot(request):
    email = loads(request.body.decode('utf-8'))['email']
    try:
        validate_email(email)
    except ValidationError:
        return Response({'message': 'Enter the valid mail', 'error': 1}, status=status.HTTP_400_BAD_REQUEST)
    if not User.objects.filter(email=email).exists():
        return Response({'message': 'No user exists with such email', 'error': 1}, status=status.HTTP_400_BAD_REQUEST)
    verify = models.MailVerification.objects.filter(user=User.objects.get(email=email), mail_type=2)
    if verify.exists():
        mail = verify[:1].get()
        mail.time_limit = timezone.now() + datetime.timedelta(days=1)
        hash_code = mail.hash_code
        mail.save()
    else:
        hash_code = sha256((str(random.getrandbits(256)) + email).encode('utf-8')).hexdigest()
        models.MailVerification(user=User.objects.get(email=email), hash_code=hash_code, mail_id=email,
                        time_limit=(datetime.datetime.now().date() + datetime.timedelta(days=1)), mail_type=2).save()
    kwargs = {'mail_type': 2, 'id': hash_code}
    mails.main(to_mail=email, **kwargs)
    return Response({'message': 'Verification mail sent, confirm it.', 'error': 0}, status=status.HTTP_200_OK)


class EmailChangeVerifyView(APIView):
    authentication_classes = []
    permission_classes = []

    def get_object(self):
        verify = models.MailVerification.objects.filter(hash_code=self.kwargs['id'])
        if verify.exists():
            return verify[0]
        else:
            return None

    def get(self, request, *args, **kwargs):
        mail = self.get_object()
        if mail is None:
            context = {'message': 'Email verification failed, please try again', 'error': 1,
                       'title': 'Email Updation'}
            return render(request, 'accounts/mail_handle.html', context)
        else:
                if mail.time_limit < timezone.now().date():
                    context = {'message': 'The one day time limit for the verification reached,'
                            ' perform the operation again', 'error': 1, 'title': 'Email Updation' }
                    return render(request, 'accounts/mail_handle.html', context)
                mail.user.email = mail.mail_id
                mail.user.save()
                mail.delete()
                context = {'message': 'Email successfully updated', 'error': 0, 'title': 'Email Updation'}
                return render(request, 'accounts/mail_handle.html', context)
