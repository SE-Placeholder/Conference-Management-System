from django.contrib import admin

from role.models import SteeringCommitteeRole, AuthorRole, ListenerRole, ReviewerRole

admin.site.register(SteeringCommitteeRole)
admin.site.register(AuthorRole)
admin.site.register(ListenerRole)
admin.site.register(ReviewerRole)