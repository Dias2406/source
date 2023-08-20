from django.contrib import admin

from student.models import Module, ModuleInfo,Affective, Cognitive, Behavioural

admin.site.register(Module)
admin.site.register(ModuleInfo)
admin.site.register(Affective)
admin.site.register(Cognitive)
admin.site.register(Behavioural)