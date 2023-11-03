from django.contrib import admin

from . import models

admin.site.register(models.CourseSelectionRequest)
admin.site.register(models.StudentCourse)
admin.site.register(models.SubstitutionRequest)
admin.site.register(models.CourseEmergencyRemovalRequest)
admin.site.register(models.CourseAppealRequest)
admin.site.register(models.TermRemovalRequest)

