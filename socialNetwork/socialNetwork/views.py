from django.http import HttpResponse
from django.shortcuts import render


def home_view(request):
    user = request.user
    hello = 'Welcome to Social Network!'

    context = {
        'user': user,
        'hello' : hello,
    }

    return render(request, 'main/home.html', context)
    #return HttpResponse("Hello World!")
    

