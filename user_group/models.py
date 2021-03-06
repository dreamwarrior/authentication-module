from django.db import models
from group.models import GroupList
from auth_jwt.models import Auth


class UserGroup(models.Model):
    group = models.ForeignKey(GroupList, on_delete=models.PROTECT)
    user = models.ForeignKey(Auth, on_delete=models.PROTECT, db_index=True)
    # createdBY = models.ForeignKey(Auth, on_delete=models.PROTECT)
    createdAT = models.DateTimeField(auto_now_add=True, auto_now=False)
    updatedAT = models.DateTimeField(auto_now_add=False, auto_now=True)

    class Meta:
        ordering = ['group', 'user']
        db_table = "user_group"
        default_permissions = []
        unique_together = ('group', 'user')