from django.contrib import admin
from .models import Accountsinformation
from .models import Supversiedpersonlist
from .models import Sensitiveevent
from .models import Twieetslists

# Register your models here.
admin.site.register(Accountsinformation)
admin.site.register(Supversiedpersonlist)
admin.site.register(Twieetslists)
admin.site.register(Sensitiveevent)
