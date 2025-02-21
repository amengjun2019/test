from django.contrib import admin

# Register your models here.

from django.contrib import admin
from custommodel.models import CustomUser
 
# Register your models here.
admin.site.register(CustomUser)