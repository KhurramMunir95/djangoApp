from django.contrib import admin
from .models import Topic, Group, Message

# Register your models here.
admin.site.register(Topic)
admin.site.register(Group)
admin.site.register(Message)