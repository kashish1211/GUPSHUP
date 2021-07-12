from django.contrib import admin
from django.contrib.admin import helpers
# from django.contrib.admin.decorators import action
from notifications.signals import notify
from .models import Post, PostComment, Report

admin.site.register(PostComment)

    # print(queryset)
    # recepient
    # message = f'deleted your '
    # notify.send(sender='Admin', recipient=recipient, verb='Post',
    # description=message)
# queryset.update(status='p')
# admin.site.add_action(mark_inappropriate)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('post_connected','reporter','status')
    search_fields= ['post_connected__id','post_connected__title','reporter__username','status']

    filter_horizontal=()
    list_filter=()
    feildsets=()

class PostAdmin(admin.ModelAdmin):
    list_display = ('title','author','date_posted')
    search_fields= ['title','author__username','date_posted','content']
    
    filter_horizontal=()
    list_filter=()
    feildsets=()
    actions = ['mark_inappropriate']
    
    
    def mark_inappropriate(self, request, queryset):
        print(queryset[0].author)
        message = f'deleted your '
        notify.send(sender='Admin', recipient=recipient, verb='Post',
        description=message)

admin.site.register(Report,ReportAdmin)
admin.site.register(Post,PostAdmin)


