from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Team(models.Model):
    name = models.CharField(max_length=100, unique=True)
    about = models.TextField()
    created_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    created_on = models.DateTimeField(default=timezone.now)
    user = models.ManyToManyField(User, related_name='team_members')
    pic = models.FileField(upload_to='group/', blank=True, null=True)

    def __str__(self):
        return self.name


class SubGroup(models.Model):
    name = models.CharField(max_length=100)
    team = models.ForeignKey(Team, null=True, on_delete=models.CASCADE)
    created_on = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.name


class Post(models.Model):
    header = models.CharField(max_length=50)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_on = models.DateTimeField(default=timezone.now)
    about = models.TextField()
    group = models.ForeignKey(SubGroup, null=True, on_delete=models.CASCADE)
    uploading = models.BooleanField(default=True)

    def __str__(self):
        return self.group.__str__() + " -- " + self.header


class PostFile(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, blank=True,  null=True)
    file = models.FileField(upload_to='uploads/', blank=True, null=True)

    def __str__(self):
        return self.post.__str__()


class PostTaggedUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'post')

    def __str__(self):
        return self.user.__str__() + " -- " + self.post.__str__()


class PostComment(models.Model):
    comment = models.TextField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, blank=True)
    postfile = models.ForeignKey(PostFile, on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
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

    class Meta:
            ordering = ['-created_on']

    def __str__(self):
        return self.comment.__str__()


class InviteLink(models.Model):
    link = models.CharField(max_length=300)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)

    def __str__(self):
        return self.link


class InviteLinkUsers(models.Model):
    link = models.ForeignKey(InviteLink, on_delete=models.CASCADE)
    email = models.EmailField(blank=True, null=True)

    def __str__(self):
        return self.link.__str__()


class Notification(models.Model):
    group = models.ForeignKey(Team, on_delete=models.CASCADE)
    created_on = models.DateTimeField(default=timezone.now)
    text = models.CharField(max_length=250)
    link = models.CharField(max_length=300, null=True, blank=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.group.__str__() + " -- " + self.text
