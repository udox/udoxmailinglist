from datetime import datetime
from django.db import models

from udoxcore.models import BaseModel, BaseManager, StatusModel, GENDER_CHOICES


class InterestGroup(StatusModel):
    sort_weight = models.IntegerField(default=100, help_text="'Heavier' groups will sink to the bottom of lists. Items with the same weight will sort alphabetically.")
    title = models.CharField(max_length=128)
    description = models.TextField(null=True, blank=True)
    
    def __unicode__(self):
        return self.title
    
    class Meta:
        ordering = ["sort_weight","title"]


class InterestItemManager(BaseManager):
    def get_query_set(self):
        return super(InterestItemManager, self).get_query_set().filter(group__status__in=[1,2])

class InterestItem(StatusModel):
    group = models.ForeignKey(InterestGroup, related_name='items', help_text="The item will not appear on site unless its parent group is also Published.")
    sort_weight = models.IntegerField(default=100, help_text="'Heavier' items will sink to the bottom of lists. Items with the same weight will sort alphabetically.")
    title = models.CharField(max_length=128)
    description = models.TextField(null=True, blank=True)
    
    objects = InterestItemManager()
    
    def __unicode__(self):
        return self.title
    
    class Meta:
        ordering = ["group__pk","sort_weight","title"]


class Member(BaseModel):
    join_date = models.DateTimeField(auto_now_add=True, editable=False, null=False)
    last_modified = models.DateTimeField(auto_now=True, editable=False, null=False)
    last_exported = models.DateTimeField(editable=False, null=True, blank=True)
    name = models.CharField(max_length=128)
    email = models.EmailField(unique=True)
    dob = models.DateField('Date of Birth', blank=True, null=True, default="YYYY-MM-DD")
    sex = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, null=True)
    mobile = models.CharField(max_length=32, blank=True, null=True)
    interest_items = models.ManyToManyField(InterestItem)
    
    def interest_groups(self):
        group_ids = self.interest_items.order_by().values_list('group__pk', flat=True)
        return InterestGroup.objects.filter(pk__in=group_ids)

    def __unicode__(self):
        return self.name
    
    class Meta:
        ordering = ["name","email"]
        get_latest_by = 'join_date'


