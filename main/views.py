from django.shortcuts import render

def home_page(request):
    template = 'home.html'
    return render(request, template)