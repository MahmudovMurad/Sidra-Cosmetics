from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def akbank_callback_handler_view(request):
    if request.method == "GET":
        print(request.GET)

    if request.method == "POST":
        print("================")
        print(request.POST)

    # If needed, handle unexpected methods
    return HttpResponseRedirect("http://64.226.106.186/")