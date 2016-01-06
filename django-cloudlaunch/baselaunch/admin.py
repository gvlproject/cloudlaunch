from django.contrib import admin

from baselaunch import models


class AppVersionInline(admin.StackedInline):
    model = models.ApplicationVersion
    extra = 1


class AppAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    inlines = [AppVersionInline]


class CloudImageInline(admin.StackedInline):
    model = models.CloudImage
    extra = 1


class CloudAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    inlines = [CloudImageInline]


class EC2Admin(admin.ModelAdmin):
    # Hide this model from main app Admin page
    # http://stackoverflow.com/questions/2431727/django-admin-hide-a-model
    get_model_perms = lambda self, req: {}


class S3Admin(admin.ModelAdmin):
    # Hide this model from main app Admin page
    # http://stackoverflow.com/questions/2431727/django-admin-hide-a-model
    get_model_perms = lambda self, req: {}

admin.site.register(models.Application, AppAdmin)
admin.site.register(models.AWS, CloudAdmin)
admin.site.register(models.EC2, EC2Admin)
admin.site.register(models.S3, S3Admin)
admin.site.register(models.OpenStack, CloudAdmin)
