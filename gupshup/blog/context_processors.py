from .models import Post

def Recent_Posts(request):
    recent = Post.objects.filter(is_appropriate = True).order_by('-date_posted')[:5]
    return {'recent':recent}

def Common_Tags(request):
    tags = Post.tags.most_common()[:10]
    return {'tags':tags}