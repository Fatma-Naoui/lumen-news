from django.shortcuts import render

def index(request):
    """Home page view"""
    return render(request, 'index.html')

def feed(request):
    """Personalized feed page view"""
    return render(request, 'feed.html')

def contact(request):
    """Contact page view"""
    return render(request, 'contact.html')