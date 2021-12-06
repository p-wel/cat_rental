from django.http import HttpResponse

def show_cats(request):
    return HttpResponse("You will see cats here")
