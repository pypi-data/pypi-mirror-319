from django.contrib import admin

from djangoldp_tems.admin import TemsModelAdmin
from djangoldp_tems_trial1.models import *

admin.site.register(Trial1Asset, TemsModelAdmin)
admin.site.register(Trial1Category, TemsModelAdmin)
admin.site.register(Trial1Format, TemsModelAdmin)
admin.site.register(Trial1Label, TemsModelAdmin)
admin.site.register(Trial1Object, TemsModelAdmin)
