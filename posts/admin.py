from django.contrib import admin
from . import models

admin.site.register(models.Team)
admin.site.register(models.InviteLink)
admin.site.register(models.InviteLinkUsers)
admin.site.register(models.Post)
admin.site.register(models.PostComment)
admin.site.register(models.PostAction)
admin.site.register(models.PostReComment)

