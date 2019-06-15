from django.contrib import admin
from .models import post,pinned,comment

# Register your models here.


admin.site.register(post)
admin.site.register(pinned)
admin.site.register(comment)