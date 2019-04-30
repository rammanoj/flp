import datetime
import random
from _sha256 import sha256
from django.contrib.auth.models import User
from django.core.validators import validate_email
from django.db.models import Q
from django.utils import timezone
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from accounts import models, mails


def password_check(password):
    if password is None:
        raise serializers.ValidationError('Fill the form completely!')
    if len(password) < 8:
        raise serializers.ValidationError('Password must have min length of 8.')
    return password


# User Login
class LoginSerializer(serializers.Serializer):
        user = serializers.CharField(required=True, max_length=50)
        password = serializers.CharField(required=True, max_length=50, validators=[password_check])
        remember_me = serializers.IntegerField(default=0)

        def validate_user(self, user):
            if user is None:
                raise serializers.ValidationError('Fill the form completely!')
            return user


# User Signup
class UserSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(max_length=50, required=True, validators=[password_check], write_only=True)
    password = serializers.CharField(max_length=50, required=True, validators=[password_check])
    email = serializers.EmailField(required=True)

    def validate_username(self, username):
        if User.objects.filter(username=username):
            raise serializers.ValidationError('already chosen!')

        if len(username) < 8:
            raise serializers.ValidationError('min length is 8')
        return username

    def validate_email(self, email):
        try:
            validate_email(email)
        except ValidationError:
            raise serializers.ValidationError('Enter a valid email')

        if User.objects.filter(email=email):
            raise serializers.ValidationError('already chosen!')
        return email

    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError('Enter same passwords both the times!')
        return attrs

    def create(self, validated_data):

        # create the user
        user = User.objects.create(username=validated_data['username'], email=validated_data['email'])
        user.set_password(validated_data['password'])
        user.is_active = False
        user.save()

        # Save the MailVerification instance
        hash_code = sha256((str(random.getrandbits(256)) + validated_data['email']).encode('utf-8')).hexdigest()
        mail = models.MailVerification(user=user, hash_code=hash_code, mail_id=validated_data['email'],
                                       time_limit=(timezone.now().date() + datetime.timedelta(days=1)), mail_type=0)
        mail.save()

        kwargs = {'mail_type': 0, 'id': hash_code}
        mails.main(to_mail=validated_data['email'], **kwargs)
        return user

    class Meta:
        model = User
        fields = ('pk', 'username', 'password', 'email', 'confirm_password')
        read_only_fields = ('pk',)


class UserSettingSerializer(serializers.ModelSerializer):

    def validate_username(self, username):
        if User.objects.filter(username=username).exclude(id=self.instance.id).exists():
            raise serializers.ValidationError('already exists!')
        if len(username) < 8:
            raise serializers.ValidationError('min length is 8')
        return username

    def validate_email(self, email):
        try:
            validate_email(email)
        except ValidationError:
            raise serializers.ValidationError('Enter a valid email')
        if User.objects.filter(email=email).exclude(id=self.instance.id).exists():
            raise serializers.ValidationError('email already exists!')
        return email

    def update(self, instance, validated_data):
        # email is changed, send a verification mail
        try:
            if instance.email != validated_data['email']:
                verify = models.MailVerification.objects.filter(Q(user=instance) & Q(mail_type=2))
                if verify.exists():
                    mail = verify[:1].get()
                    mail.email = validated_data['email']
                    mail.time_limit = datetime.datetime.now().date() + datetime.timedelta(days=1)
                    mail.save()
                    hash_code = mail.hash_code
                else:
                    hash_code = sha256(
                        (str(random.getrandbits(256)) + validated_data['email']).encode('utf-8')).hexdigest()
                    mail = models.MailVerification(user=instance, hash_code=hash_code, mail_id=validated_data['email'],
                                                   time_limit=(datetime.datetime.now().date() + datetime.timedelta(
                                                       days=1)), mail_type=2)
                    mail.save()
                kwargs = {'mail_type': 1, 'id': hash_code}
                mails.main(to_mail=validated_data['email'], **kwargs)
                validated_data['email'] = instance.email
        except KeyError:
            pass
        return super(UserSettingSerializer, self).update(instance, validated_data)

    class Meta:
        model = User
        fields = ('pk', 'username', 'email')
        read_only_fields = ('pk',)


class UserPasswordUpdateSerializer(serializers.ModelSerializer):
    new_password = serializers.CharField(write_only=True, required=True)
    confirm_password = serializers.CharField(write_only=True, required=True)
    password = serializers.CharField(write_only=True, required=True)

    def validate(self, attrs):
        if len(attrs['new_password']) < 8:
            raise serializers.ValidationError('Password length can\'t be less than 8')
        if attrs['new_password'] != attrs['confirm_password']:
            raise serializers.ValidationError('Confirm your password correctly')
        return attrs

    class Meta:
        model = User
        fields = ('password', 'confirm_password', 'new_password')


class ForgotPasswordUpdateSerailizer(serializers.Serializer):
    password1 = serializers.CharField(write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True)
