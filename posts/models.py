from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Team(models.Model):
    name = models.CharField(max_length=100, unique=True)
    about = models.TextField()
    created_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    created_on = models.DateTimeField(default=timezone.now)
    user = models.ManyToManyField(User, related_name='team_members')

    def __str__(self):
        return self.name


class Post(models.Model):
    header = models.CharField(max_length=50)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_on = models.DateTimeField(default=timezone.now)
    about = models.TextField()
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    file = models.FileField(upload_to='uploads/')

    def __str__(self):
        return self.team.__str__() + " -- " + self.header


class PostComment(models.Model):
    comment = models.TextField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    created_on = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.post.__str__() + " " + self.user.__str__()


class PostAction(models.Model):
    action = models.TextField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_on = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('post', 'user')

    def __str__(self):
        return self.post.__str__() + " " + self.user.__str__()


class PostReComment(models.Model):
    comment = models.ForeignKey(PostComment, on_delete=models.CASCADE)
    re_comment = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_on = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.comment.__str__()


class InviteLink(models.Model):
    link = models.CharField(max_length=300)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)

    def __str__(self):
        return self.link


class InviteLinkUsers(models.Model):
    link = models.ForeignKey(InviteLink, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.link.__str__()


class Notification(models.Model):
    group = models.ForeignKey(Team, on_delete=models.CASCADE)
    created_on = models.DateTimeField(default=timezone.now)
    text = models.CharField(max_length=250)
    link = models.CharField(max_length=300, null=True, blank=True)

    def __str__(self):
        return self.group.__str__() + " -- " + self.text


