from django.contrib import admin

# Register your models here.
from users.models import UserAccount

admin.site.register(UserAccount)
