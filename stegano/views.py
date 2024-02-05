import io
from django.shortcuts import HttpResponse, render
from .utils import hide, retr


def index(request):
    return render(request, "index.html")


def encode(request):
    if request.method == "POST":
        message = request.POST.get("message")
        image = request.FILES["image"]
        img = hide(image,message)
        output = io.BytesIO()
        img.save(output, 'PNG')
        contents = output.getvalue()
        output.close()
        rea_response= HttpResponse(contents, content_type='image/jpg')
        rea_response['Content-Disposition'] = 'attachment; filename={}'.format('encoded.jpg')
        return rea_response

    return render(request, "encode.html")


def decode(request):
    if request.method == "POST":
        image = request.FILES["image"]
        result = retr(image)
        return render(request, "decode.html", {"result":result})
        
    return render(request, "decode.html")