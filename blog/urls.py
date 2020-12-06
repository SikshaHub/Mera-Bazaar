from django.urls import path
from .views import index, blogPost

urlpatterns = [
    path('', index, name="BlogHome"),
    path('post/<int:id>', blogPost, name="BlogPost"),
]