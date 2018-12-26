from django.contrib import admin
from .models import User
from .models import Manager
from .models import Doctor
from .models import Accountant
from .models import Reception
from .models import Patient
from .models import DrugStore

admin.site.register(User)
admin.site.register(Manager)
admin.site.register(Doctor)
admin.site.register(Accountant)
admin.site.register(Reception)
admin.site.register(Patient)
admin.site.register(DrugStore)
