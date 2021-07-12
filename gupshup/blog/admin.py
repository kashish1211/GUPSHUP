from django.contrib import admin
from .models import Post, PostComment, Report

admin.site.register(PostComment)


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
admin.site.register(Report,ReportAdmin)
admin.site.register(Post,PostAdmin)