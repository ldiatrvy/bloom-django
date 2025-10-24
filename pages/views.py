from django.shortcuts import render

def contacts(request):
    return render(request, 'pages/contacts.html')

def about(request):
    return render(request, 'pages/about.html')

def faq(request):
    return render(request, 'pages/faq.html')
