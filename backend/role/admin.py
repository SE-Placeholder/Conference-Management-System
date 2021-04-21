from django.contrib import admin

from role.models import SteeringCommitteeRole, AuthorRole, ListenerRole

admin.site.register(SteeringCommitteeRole)
admin.site.register(AuthorRole)
admin.site.register(ListenerRole)
