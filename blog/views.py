from django.shortcuts import render
from .models import BlogPost

# Create your views here.
def index(request):
    template = 'blog/index.html'
    blog_post = BlogPost.objects.all()
    print(blog_post)
    context = {
        'blogpost': blog_post,
    }
    return render(request, template, context)

def blogPost(request, id):
    template = 'blog/blogpost.html'
    post = BlogPost.objects.filter(post_id = id)[0]
    context = {
        'post': post,
    }
    return render(request, template, context)
