from .models import Post, Category

def Recent_Posts(request):
    recent = Post.objects.filter(is_appropriate = True).order_by('-date_posted')[:5]
    return {'recent':recent}

def Common_Tags(request):
    tags = Post.tags.most_common()[:10]
    return {'tags':tags}

def Common_Categories(request):
    categories = Category.objects.all().order_by('-num_of_posts')
    return {'categories_6':categories[:6],'categories_rest':categories[6:]}