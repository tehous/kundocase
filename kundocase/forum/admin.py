from django.contrib import admin
from kundocase.forum.models import Topic, PostModel



class AdminManager(admin.ModelAdmin):
    def get_queryset(self, request):
        qs = self.model.adminmanager.get_queryset()
        ordering = self.get_ordering(request)
        if ordering:
            qs = qs.order_by(*ordering)
        return qs 

admin.site.register(Topic, AdminManager)
admin.site.register(PostModel, AdminManager)

