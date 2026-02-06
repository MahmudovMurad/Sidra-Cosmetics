from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def callback_view(request):
    if request.method == "GET":
        print(request.GET)

    if request.method == "POST":
        print("================")
        print(request.POST)

    # If needed, handle unexpected methods
    return HttpResponseRedirect("https://sidra-kozmetik.com/")